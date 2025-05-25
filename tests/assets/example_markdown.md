# Study Buddy

Welcome to **Study Buddy**! This project is designed to help students organize their study sessions, track progress, and collaborate with peers. Whether you’re preparing for exams, managing assignments, or just looking to boost productivity, Study Buddy has you covered.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- 📅 **Session Scheduling:** Plan and schedule study sessions with reminders.
- 📝 **Task Management:** Create, edit, and track tasks and assignments.
- 📊 **Progress Tracking:** Visualize your study progress with charts and stats.
- 🤝 **Collaboration:** Invite friends to study groups and share resources.
- 🔒 **Secure:** User authentication and data privacy.

---

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v16+)
- [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)
- [MongoDB](https://www.mongodb.com/) (for backend)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/study-buddy.git
    cd study-buddy
    ```

2. **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```

3. **Set up environment variables:**
    - Copy `.env.example` to `.env` and fill in your configuration.

4. **Start the development server:**
    ```bash
    npm run dev
    # or
    yarn dev
    ```

---

## Usage

- Access the app at `http://localhost:3000`
- Register a new account or log in.
- Create study sessions, add tasks, and invite friends.
- Track your progress on the dashboard.

---

## Configuration

Edit the `.env` file to configure:

- `MONGODB_URI`
- `JWT_SECRET`
- `PORT`
- `EMAIL_SERVICE` (optional)

---

## API Reference

### Authentication

- `POST /api/auth/register` — Register a new user
- `POST /api/auth/login` — Log in

### Sessions

- `GET /api/sessions` — List sessions
- `POST /api/sessions` — Create session

### Tasks

- `GET /api/tasks` — List tasks
- `POST /api/tasks` — Create task

---

## Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Open a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## Contact

- **Author:** Sebastian Sotomayor
- **Email:** sebastian@example.com
- **GitHub:** [@yourusername](https://github.com/yourusername)

---

Happy studying! 🎓