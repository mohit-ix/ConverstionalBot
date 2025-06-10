# ProPal AI Assignment

This is an assignment provided by ProPal AI on Developing a Conversational Pipeline:
    STT -> LLM -> TTS
Using LiveKit

And after the conversation ends, capture metrics in an excel file which includes EOU, TTFB, TTFT, and total latency.

## My Solution.

For my solution to this Assignment, I have developed the pipeline using LiveKit.
I have used:
    LLM - Groq(Llama-3.3-70b-versatile)
    STT - Groq(Whisper Large V3 Turbo)
    TTS - ElevenLabs(Jessica's Voice)
    (Groq also provides TTS service using playai-tts but it is not as good as Elevenlabs and its context window and daily usage is also very low).

As for the metrics, I capture the metrics after every sentence is done and prints it in the console. I looked into the documentation and other methods to export it to excel or to only separate out the necessary values but I was not able to find it.
As for the latency, The total latency which is calculated as:
    total_latency = eou + ttfb + ttft

The total latency is around 2.5 to 5 seconds. But it can be more for longer sentences and less for short sentences.
The pipeline also has interuption mechanism i.e., The agent will stop talking if you try to say something mid sentence.