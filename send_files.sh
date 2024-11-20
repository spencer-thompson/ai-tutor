rsync -avrPluxz \
    --include='deploy.yaml' \
    --include='develop.yaml' \
    --include='.env' \
    --include='mongo/***' \
    --include='backend/***' \
    --include='compose/***' \
    --include='streamlit/***' \
    --exclude='*' \
    . aitutor:/home/sthom/aitutor/
