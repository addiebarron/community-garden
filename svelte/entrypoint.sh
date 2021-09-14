if [[ $APP_ENV == "dev" ]]; then
    npm run dev
else
    npm run build && npm start
fi