# Mozio backend project

Mozio Backend Potential hire Project 2.0

# Tech stack

## Backend

- Python 3.6
- Django 2.0
- Postgres 10

# Workflow

- Create a provider using `/api/v1/providers/`.
- The result provider will contain a token which has to be send in the header `X-Api-Token`
- All `GET` requests don't need authentication.
- To search using a point(lat, lng) use `/api/v1/service-areas/?lat={}&lng={}`.

# Possible improvements

- Use an hypermedia format.
