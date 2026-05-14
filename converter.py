import os
import zipfile
import io
import json
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from PIL import Image
import fitz

SAVED_PROFILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles.json")

MANHWA_RATIO_THRESHOLD = 2.0
MANHWA_PAGE_THRESHOLD = 0.3

DEVICE_PROFILES = {
    "PocketBook Verse Pro Color": (1072, 1448),
    "PocketBook InkPad Color 3": (1404, 1872),
    "PocketBook Era": (1264, 1680),
    "PocketBook Touch HD 3": (1072, 1448),
    "Kindle Basic 11 (2024)": (1072, 1448),
    "Kindle Paperwhite 5 (2021)": (1236, 1648),
    "Kindle Paperwhite 6 (2024)": (1272, 1696),
    "Kindle Scribe (2022)": (1860, 2480),
    "Kindle Scribe 3 (2025)": (1986, 2648),
    "Kindle Oasis 2/3": (1264, 1680),
    "Kindle Voyage": (1072, 1448),
    "Kindle Colorsoft": (1272, 1696),
    "Kobo Libra Colour": (1264, 1680),
    "Kobo Clara BW": (1072, 1448),
    "Kobo Clara Colour": (1072, 1448),
    "Kobo Elipsa 2E": (1404, 1872),
    "Kobo Sage": (1440, 1920),
    "Kobo Forma": (1440, 1920),
    "reMarkable 2": (1404, 1872),
    "reMarkable Paper Pro": (1620, 2160),
    "Custom": (0, 0),
}


def load_saved_profiles():
    if not os.path.exists(SAVED_PROFILES_PATH):
        return {}
    try:
        with open(SAVED_PROFILES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_profile(name, width, height):
    profiles = load_saved_profiles()
    profiles[name] = [width, height]
    with open(SAVED_PROFILES_PATH, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)


def delete_saved_profile(name):
    profiles = load_saved_profiles()
    profiles.pop(name, None)
    with open(SAVED_PROFILES_PATH, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)


def get_all_profiles():
    built_in = dict(DEVICE_PROFILES)
    saved = load_saved_profiles()
    for name, (w, h) in saved.items():
        built_in[name] = (w, h)
    return built_in


def detect_mode(pdf_path):
    doc = fitz.open(pdf_path)
    tall_pages = 0
    total = min(50, doc.page_count)
    for i in range(total):
        r = doc[i].rect
        if r.height > r.width * MANHWA_RATIO_THRESHOLD:
            tall_pages += 1
    doc.close()
    ratio = tall_pages / total if total > 0 else 0
    if ratio >= MANHWA_PAGE_THRESHOLD:
        return "manhwa"
    return "manga"


def split_tall_page(img_pil, page_rect):
    w, h = img_pil.size
    pdf_w, pdf_h = page_rect.width, page_rect.height
    scale = w / pdf_w
    section_height = int(pdf_h * scale)
    if h <= section_height * 1.3:
        return [img_pil]
    num_sections = round(h / section_height)
    if num_sections < 2:
        return [img_pil]
    section_h = h // num_sections
    sections = []
    for i in range(num_sections):
        top = i * section_h
        bottom = top + section_h if i < num_sections - 1 else h
        section = img_pil.crop((0, top, w, bottom))
        sections.append(section)
    return sections


def _ensure_rgb(pil_img):
    if pil_img.mode in ("P", "I", "1"):
        return pil_img.convert("RGB")
    if pil_img.mode == "CMYK":
        return pil_img.convert("RGB")
    if pil_img.mode == "RGBA":
        bg = Image.new("RGB", pil_img.size, (255, 255, 255))
        bg.paste(pil_img, mask=pil_img.split()[3])
        return bg
    return pil_img


def apply_gamma(pil_img, gamma):
    if gamma is None or gamma == 1.0:
        return pil_img
    lut = [min(255, int(round(pow(i / 255.0, gamma) * 255))) for i in range(256)]
    if pil_img.mode == "L":
        return pil_img.point(lut)
    if pil_img.mode == "RGB":
        return pil_img.point(lut * 3)
    return pil_img


def apply_grayscale(pil_img):
    if pil_img.mode == "L":
        return pil_img
    return pil_img.convert("L")


def apply_autocontrast(pil_img, cutoff=2):
    if pil_img.mode == "RGB":
        bands = list(pil_img.split())
        for i in range(3):
            bands[i] = _autocontrast_band(bands[i], cutoff)
        return Image.merge("RGB", bands)
    if pil_img.mode == "L":
        return _autocontrast_band(pil_img, cutoff)
    return pil_img


def _autocontrast_band(band, cutoff):
    hist = band.histogram()
    total = sum(hist)
    if total == 0:
        return band
    lo = 0
    acc = 0
    cutoff_pixels = int(total * cutoff / 100)
    for i, h in enumerate(hist):
        acc += h
        if acc > cutoff_pixels:
            lo = i
            break
    hi = 255
    acc = 0
    for i, h in enumerate(reversed(hist)):
        acc += h
        if acc > cutoff_pixels:
            hi = 255 - i
            break
    if lo >= hi:
        return band
    lut = [0] * lo + [min(255, int(round((i - lo) / (hi - lo) * 255))) for i in range(lo, hi + 1)] + [255] * (256 - hi - 1)
    return band.point(lut)


def resize_for_device(pil_img, target_w, target_h):
    if target_w <= 0 or target_h <= 0:
        return pil_img
    img_w, img_h = pil_img.size
    scale = min(target_w / img_w, target_h / img_h)
    if scale >= 1.0:
        return pil_img
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    return pil_img.resize((new_w, new_h), Image.LANCZOS)


def process_image(pil_img, settings):
    img = _ensure_rgb(pil_img)
    if settings.get("autocontrast"):
        img = apply_autocontrast(img)
    gamma = settings.get("gamma")
    if gamma is not None and gamma != 1.0:
        img = apply_gamma(img, gamma)
    if settings.get("grayscale"):
        img = apply_grayscale(img)
    tw = settings.get("target_w", 0)
    th = settings.get("target_h", 0)
    if tw > 0 and th > 0:
        img = resize_for_device(img, tw, th)
    return img


def extract_page_image(doc, page_num):
    page = doc[page_num]
    imgs = page.get_images(full=True)
    if imgs:
        for img_info in imgs:
            try:
                d = doc.extract_image(img_info[0])
                pil_img = Image.open(io.BytesIO(d["image"]))
                return _ensure_rgb(pil_img), True
            except Exception:
                continue
    pix = page.get_pixmap(dpi=300)
    pil_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return pil_img, False


def _process_page_thread(pdf_path, page_num, is_manhwa, page_rect, settings):
    doc = fitz.open(pdf_path)
    try:
        pil_img, direct = extract_page_image(doc, page_num)
        if is_manhwa:
            sections = split_tall_page(pil_img, page_rect)
        else:
            sections = [pil_img]
        results = []
        for sec_pil in sections:
            sec_pil = process_image(sec_pil, settings)
            buf = io.BytesIO()
            sec_pil.save(buf, format="JPEG", quality=92)
            results.append(buf.getvalue())
        return (page_num, results, None)
    except Exception as e:
        return (page_num, [], str(e))
    finally:
        doc.close()


def convert_pdf_to_cbz(pdf_path, output_dir=None, mode="auto", settings=None, on_progress=None):
    pdf_path = os.path.abspath(pdf_path)
    name = os.path.splitext(os.path.basename(pdf_path))[0]
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        cbz_path = os.path.join(output_dir, f"{name}.cbz")
    else:
        cbz_path = os.path.join(os.path.dirname(pdf_path), f"{name}.cbz")

    doc = fitz.open(pdf_path)
    total = doc.page_count

    if mode == "auto":
        mode = detect_mode(pdf_path)

    is_manhwa = mode == "manhwa"
    page_rects = [doc[i].rect for i in range(total)]
    doc.close()

    if settings is None:
        settings = {}

    all_sections = {}
    failures = []
    num_workers = min(8, multiprocessing.cpu_count())

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        fn = partial(_process_page_thread, pdf_path=pdf_path, is_manhwa=is_manhwa, settings=settings)
        futures = {
            executor.submit(fn, page_num=i, page_rect=page_rects[i]): i
            for i in range(total)
        }
        done = 0
        for future in as_completed(futures):
            page_num = futures[future]
            try:
                pn, sections, err = future.result()
                if err:
                    failures.append((pn, err))
                else:
                    all_sections[pn] = sections
            except Exception as e:
                failures.append((page_num, str(e)))
            done += 1
            if on_progress:
                on_progress(done, total)

    all_images = []
    for i in range(total):
        if i in all_sections:
            for img_bytes in all_sections[i]:
                all_images.append(img_bytes)

    with zipfile.ZipFile(cbz_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, img_bytes in enumerate(all_images):
            zf.writestr(f"page_{idx+1:04d}.jpg", img_bytes)

    return {
        "cbz_path": cbz_path,
        "total_pages": total,
        "total_images": len(all_images),
        "failures": failures,
    }


def generate_processed_preview(pdf_path, page_num, settings, max_size=(300, 400)):
    doc = fitz.open(pdf_path)
    try:
        pil_img, _ = extract_page_image(doc, page_num)
        processed = process_image(pil_img, settings)
        processed.thumbnail(max_size, Image.LANCZOS)
        buf = io.BytesIO()
        processed.save(buf, format="PNG")
        buf.seek(0)
        return buf
    finally:
        doc.close()


def generate_side_by_side_preview(pdf_path, page_num, settings, thumb_size=(200, 280)):
    doc = fitz.open(pdf_path)
    try:
        pil_img, _ = extract_page_image(doc, page_num)
        orig = _ensure_rgb(pil_img)
        processed = process_image(pil_img, settings)
        orig.thumbnail(thumb_size, Image.LANCZOS)
        processed.thumbnail(thumb_size, Image.LANCZOS)
        w = orig.width + processed.width + 8
        h = max(orig.height, processed.height)
        canvas = Image.new("RGB", (w, h), (245, 245, 245))
        canvas.paste(orig, (0, 0))
        canvas.paste(processed, (orig.width + 8, 0))
        buf = io.BytesIO()
        canvas.save(buf, format="PNG")
        buf.seek(0)
        return buf
    finally:
        doc.close()
