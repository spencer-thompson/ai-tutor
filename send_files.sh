rsync -avrPluxz \
    --exclude='*/node_modules/***' \
    --include='deploy.yaml' \
    --include='develop.yaml' \
    --include='.env' \
    --include='svelte/***' \
    --include='mongo/***' \
    --include='backend/***' \
    --include='compose/***' \
    --include='plausible/***' \
    --include='streamlit/***' \
    --include='data/***' \
    --include='python_sandbox/***' \
    --exclude='*' \
    . aitutor:/home/sthom/aitutor/
