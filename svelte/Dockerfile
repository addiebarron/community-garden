FROM mhart/alpine-node:16

WORKDIR /app
# Copy all local files into the image.
COPY . .

EXPOSE 3000
ENTRYPOINT ["sh", "entrypoint.sh"]
