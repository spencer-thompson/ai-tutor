rsync -avrPluxz \
    --include='deploy.yaml' \
    --include='develop.yaml' \
    --include='.env' \
    --include='mongo/***' \
    --include='backend/***' \
    --include='compose/***' \
    --include='plausible/***' \
    --include='streamlit/***' \
    --include='data/***' \
    --exclude='*' \
    . aitutor:/home/sthom/aitutor/
