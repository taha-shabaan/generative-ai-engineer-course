# Build a Weather AI Agent (Real Data)

A LangChain agent powered by Google Gemini that answers weather questions using
**live data** from the [OpenWeatherMap API](https://openweathermap.org/current).

## How it works

1. The agent receives a natural-language question (e.g. *"What is the weather in Tokyo?"*).
2. Gemini decides to call the `get_weather` tool.
3. `get_weather` requests real current weather from OpenWeatherMap.
4. The agent formats the answer as: `Weather in {city} is {condition}, and the temperature is {temperature}.`

## Project structure

```
03-build_weather_ai_agent/
└── main.py   # agent, weather tool, and CLI entry point
```

## Setup

### 1. Install dependencies

From the repository root:

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your keys:

```bash
GOOGLE_API_KEY=your-google-gemini-key
OPENWEATHER_API_KEY=your-openweathermap-key
```

- `GOOGLE_API_KEY` — get one at <https://aistudio.google.com/app/apikey>
- `OPENWEATHER_API_KEY` — sign up free at <https://home.openweathermap.org/users/sign_up>

> `.env` is git-ignored and must never be committed.

### 3. Run the agent

```bash
python 03-build_weather_ai_agent/main.py
```

Then enter a query:

```
Enter your query: What is the weather in Cairo?
Weather in Cairo is clear sky, and the temperature is 24.42°C.
```

## Example output

```
Enter your query: What is the weather in Tokyo?
Weather in Tokyo is clear sky, and the temperature is 10.26°C.
```

## Notes

- The tool uses `units=metric`, so temperatures are returned in Celsius.
- Network/API errors surface via `response.raise_for_status()`.
- The agent runs from the repository root; `load_dotenv()` finds the root `.env` automatically.
