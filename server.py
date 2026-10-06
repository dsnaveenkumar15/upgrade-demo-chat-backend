"""A tiny chat backend that streams assistant replies, written for openai 3.15 (an older release on purpose)."""
from openai import OpenAI
from openai.lib.streaming import AssistantEventHandler

client = OpenAI()


class Collector(AssistantEventHandler):
    """Collects streamed text from an assistant run."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def on_text_delta(self, delta, snapshot) -> None:
        self.parts.append(delta.value)


def reply(thread_id: str, assistant_id: str) -> str:
    handler = Collector()
    with client.beta.threads.runs.stream(thread_id=thread_id, assistant_id=assistant_id, event_handler=handler) as stream:
        stream.until_done()
    return "".join(handler.parts)
