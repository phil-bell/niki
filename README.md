# niki-server

Sister server to the Niki app for managing plex content.

## Operation

```
docker run \
    -d \
    -v /mnt/a/movie/:/mnt/a/movie/ \
    -v /mnt/c/tv/:/mnt/c/tv/ \
    -e SERVER_KEY=abc \
    -e SERVER_SECRET=xyz \
    --network host \
    philbell/niki-server:latest
```