mkdir -p ~/.streamlit/ && \
echo -e "\
[general]\n\
email = \"your@domain.com\"\n\
" > ~/.streamlit/credentials.toml && \
echo -e "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = 8501\n\
" > ~/.streamlit/config.toml

