# Community Garden

🌻🌼🌱🌷🌻🌼🌱🌷🌻🌼🌱🌷🌻🌼🌱🌷🌻🌼🌱🌷🌻🌼🌱🌷🌻🌼🌱🌷🌻

**Community Garden is an experimental game and an exploration of web community models.**

It is also a learning project designed to allow me to explore full-stack app development, specifically in integrating a modern frontend web framework with a robust backend, as well as best practices in UX & accessibility, authentication & security, Python OOP, and general systems design. The app's frontend (built in SvelteKit) talks to a Django backend, which uses PostgreSQL as its database. Within the Django backend, [Channels](https://channels.readthedocs.io/en/stable/) handles WebSocket connections.

## Interface

The UI is compromised of 4 main parts:

- Garden grid
  - Each grid square ("plot") can optionally contain soil and a plant
    - A plant cannot be added without adding soil
    - Soil has an associated water level. Water can be added, and it decreases naturally over time
    - Each plant has an associated health level, which increases or decreases based on factors including water level
  - Each player has a cursor that can be moved by clicking or using the arrow keys
    - Players can see other players' cursors
- Command list
  - Displays the commands associated with the currently selected square
  - The command list is updated as the cursor moves
  - Each command can be executed be clicking it, or by pressing the number key listed next to the command
- History log
  - A running log of all actions taken within the game
  - Each entry lists the timestamp and user associated with the action
- Chat
  - A simple real-time chat window for all users

## Design philosophy

The design of this app is informed by my experience in game studies and critical theory. I hoped to create an experience that encourages communitarian, mutualistic, and coordinated behavior through its design, rather than through strict guidelines or moderation (though some version of these will probably need to come into play eventually).

The nature of the app requires users to coordinate their tending of the plants, since any user can take any action toward any plant, but over-tending (e.g. through overwatering) will cause a plant to die. If a player takes intentionally destructive action toward the garden, their actions will be logged publicly and kept in record forever. I'll probably add a voting system for removing users permanently, but that is outside the current scope of the project.

## Development

The app uses Docker for development. There is not currently a production version.

To build and run the app locally, run

```
docker-compose up -d
```
