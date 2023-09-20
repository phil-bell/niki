# niki-server

Sister server to the Niki app for managing plex content.

## Operation

### Docker
```
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