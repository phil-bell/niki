# niki-server

Sister server to the Niki app for managing plex content.

## Operation

### Docker
```bash
docker run \
  -d \
  -v /mnt/a/movie/:/mnt/a/movie/ \
  -v /mnt/b/tv/:/mnt/b/tv/ \
  -e SERVER_KEY=abc \
  -e SERVER_SECRET=xyz \
  --network host \
  philbell/niki-server:latest
```

**Note:** a tailered command to your server can be found on the server page

## Contributing

### Building
```bash
docker buildx create --use
```
```bash
docker buildx build --push --platform linux/arm64,linux/amd64 --tag philbell/niki-server:1.1.2 -t philbell/niki-server:latest .
```
```bash
docker context use default
```
```bash
docker buildx use default
```