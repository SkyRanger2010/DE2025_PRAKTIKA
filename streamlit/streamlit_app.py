import streamlit as st
import requests
import math
import chardet

API_URL = "http://keyword_search:80/keyword_search"

st.title("Поиск по ключевым словам")

def to_utf8(s: str) -> str:
    """
    Преобразует строку в utf-8, если она была введена в другой кодировке.
    """
    if not s:
        return ""
    try:
        # Если строка уже str (unicode), пробуем перекодировать через bytes
        if isinstance(s, str):
            # Пробуем определить кодировку, если есть подозрение на не-utf8
            detected = chardet.detect(s.encode(errors='replace'))
            encoding = detected.get("encoding", "utf-8")
            if encoding.lower() != "utf-8":
                return s.encode(encoding).decode("utf-8", errors="replace")
        return s
    except Exception:
        return s

keywords = st.text_area("Введите одно или несколько ключевых слов (через запятую):")
keywords = to_utf8(keywords)

per_page_options = [1, 5, 20, 100, "все"]
# По умолчанию "все"
if "per_page" not in st.session_state:
    st.session_state["per_page"] = "все"
per_page = st.selectbox(
    "Элементов на страницу",
    per_page_options,
    index=per_page_options.index(st.session_state["per_page"]),
    key="per_page_select"
)
if per_page != st.session_state.get("per_page"):
    st.session_state["per_page"] = per_page
    st.session_state["page"] = 1

if "page" not in st.session_state:
    st.session_state["page"] = 1

if st.button("Поиск"):
    st.session_state["search"] = True
    st.session_state["page"] = 1
    st.session_state["search_keywords"] = keywords

if st.session_state.get("search", False):
    keywords = st.session_state["search_keywords"]
    per_page = st.session_state["per_page"]

    params_count = {
        "keywords": keywords,
        "start_idx": 0,
    }
    response_count = requests.get(API_URL, params=params_count)
    if response_count.status_code == 200:
        total_count = response_count.json()["count"]

        if per_page == "все":
            params = {
                "keywords": keywords,
                "start_idx": 0,
            }
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['count'] == 0:
                    st.info("Записи не найдены")
                else:
                    st.success(f"Найдено записей: {data['count']}")
                    with st.container():
                        for user in data["res"]:
                            st.json(user)
            else:
                st.error(f"Ошибка: {response.status_code} — {response.text}")
        else:
            per_page_int = int(per_page)
            total_pages = max(1, math.ceil(total_count / per_page_int))

            # Всегда используем только st.session_state["page"]
            if "page" not in st.session_state:
                st.session_state["page"] = 1

            # Навигационные кнопки
            nav_cols = st.columns([1,1,1,1,1], gap="small")
            with nav_cols[0]:
                if st.button("⏮ 1", key="first", use_container_width=True):
                    st.session_state["page"] = 1
            with nav_cols[1]:
                if st.button("◀", key="prev", use_container_width=True):
                    if st.session_state["page"] > 1:
                        st.session_state["page"] -= 1
            with nav_cols[3]:
                if st.button("▶", key="next", use_container_width=True):
                    if st.session_state["page"] < total_pages:
                        st.session_state["page"] += 1
            with nav_cols[4]:
                if st.button(f"⏭ {total_pages}", key="last", use_container_width=True):
                    st.session_state["page"] = total_pages

            # После обработки кнопок используйте только st.session_state["page"]
            page = st.session_state["page"]
            total_pages = max(1, math.ceil(total_count / per_page_int))

            with nav_cols[2]:
                st.button(f"Стр. {page} / {total_pages}", key="current", use_container_width=True, disabled=True)

            start_idx = (page - 1) * per_page_int
            end_idx = start_idx + per_page_int

            params = {
                "keywords": keywords,
                "start_idx": start_idx,
                "end_idx": end_idx
            }
            response = requests.get(API_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['count'] == 0:
                    st.info("Записи не найдены")
                else:
                    st.info(
                        f"Показаны записи с {start_idx+1} по {min(end_idx, total_count)} из {total_count}"
                    )
                    for user in data["res"]:
                        st.json(user)
            else:
                st.error(f"Ошибка: {response.status_code} — {response.text}")
    else:
        st.error(f"Ошибка: {response_count.status_code} — {response_count.text}")