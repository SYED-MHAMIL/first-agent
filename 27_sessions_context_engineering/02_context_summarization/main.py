import asyncio
from collections import deque
from typing import Optional, List, Tuple, Dict, Any

from llm_summarization import LLMSummarizer

Record = Dict[str, Dict[str, Any]]  # {"msg": {...}, "meta": {...}}

class SummarizingSession:
    """
    Session that keeps only the last N *user turns* verbatim and summarizes the rest.

    - A *turn* starts at a real user message and includes everything until the next real user message.
    - When the number of real user turns exceeds `context_limit`, everything before the earliest
      of the last `keep_last_n_turns` user-turn starts is summarized into a synthetic user→assistant pair.
    
    - Stores full records (message + metadata). Exposes:
        • get_items():           model-safe messages only (no metadata)
        • get_full_history():    [{"message": msg, "metadata": meta}, ...]
    """

    # Only these keys are ever sent to the model; the rest live in metadata.
    _ALLOWED_MSG_KEYS = {"role", "content", "name"}

    def __init__(
       self,
       keep_last_N_turns : int  =3,
       context_limits : int =3  ,  
       summerizer : Optional["LLMSummarizer"] = None ,   
       session_id  : Optional[str] = None  
    ):
        assert  keep_last_N_turns >=1 
        assert  context_limits >=1 
        assert  keep_last_N_turns <= context_limits , "keep_last_n_turns should not be greater than context_limit"
        
        self.keep_last_n_turns = keep_last_N_turns 
        self.context_limit
        self.summarizer =summerizer
        self.session_id = session_id or "default"
        
        
        self._record:deque[Record]  =deque()
        self._lock = asyncio.Lock()

  
        

    # --------- public API used by your runner ---------
    async def get_items(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Return model-safe messages only (no metadata)."""
        async with self._lock:
               data =list(self._record)
               msgs = [self._sanitize_for_model(rec["msg"]) for rec in data]
               return msgs[-limit] if limit else msgs
               
    async def add_items(self, items: List[Dict[str, Any]]) -> None:
        """Append new items and, if needed, summarize older turns."""
        # 1) Ingest items
        async with self._lock:
            print("ADD_ITEM_SESSION " , items)
        
        
    async def pop_item(self) -> Optional[Dict[str, Any]]:
        """Pop the latest message (model-safe), if any."""
        async with self._lock:
            if not self._records:
                return None
            rec = self._records.pop()
            return dict(rec["msg"])


    async def clear_session(self) -> None:
        """Remove all records."""
        async with self._lock:
            self._records.clear()

    def set_max_turns(self, n: int) -> None:
        """
        Back-compat shim for old callers: update `context_limit`
        and clamp `keep_last_n_turns` if needed.
        """
        assert n >= 1
        self.context_limit = n
        if self.keep_last_n_turns > self.context_limit:
            self.keep_last_n_turns = self.context_limit


    async def _summarize(self, prefix_msgs: List[Dict[str, Any]]) -> Tuple[str, str]:
        """
        Ask the configured summarizer to compress the given prefix.
        Uses model-safe messages only. If no summarizer is configured,
        returns a graceful fallback.
        """
        if not self.summarizer:
            return ("Summarize the conversation we had so far.", "Summary unavailable.")
        clean_prefix = [self._sanitize_for_model(m) for m in prefix_msgs]
        return await self.summarizer.summarize(clean_prefix)

session = SummarizingSession(
    keep_last_n_turns=2,
    context_limit=4,
    summarizer=LLMSummarizer()
)

async def main():
    print(f"\n\n[LEN MESSAGES]: 10\n\n")
    # Example flow
    await session.add_items([{"role": "user", "content": "Hi, my router won't connect. by the way, I am using Windows 10. I tried troubleshooting via your FAQs but I didn't get anywhere. This is my third tiem calling you. I am based in the US and one of Premium customers."}])
    await session.add_items([{"role": "assistant", "content": "Let's check your firmware version."}])
    await session.add_items([{"role": "user", "content": "Firmware v1.0.3; still failing."}])
    await session.add_items([{"role": "assistant", "content": "Try a factory reset."}])
    await session.add_items([{"role": "user", "content": "Reset done; error 42 now."}])
    await session.add_items([{"role": "assistant", "content": "Try to install a new firmware."}])
    await session.add_items([{"role": "user", "content": "I tried but I got another error now."}])
    await session.add_items([{"role": "assistant", "content": "Can you please provide me with the error code?"}])
    await session.add_items([{"role": "user", "content": "It says 404 not found when I try to access the page."}])
    await session.add_items([{"role": "assistant", "content": "Are you connected to the internet?"}])
    await session.add_items([{"role": "user", "content": "Yes, I am connected to the internet."}])
    await session.add_items([{"role": "assistant", "content": "Great, I will help you with your internet connection."}])
    await session.add_items([{"role": "user", "content": "Thank you."}])
    await session.add_items([{"role": "assistant", "content": "You're welcome. Is there anything else I can help you with?"}])
    await session.add_items([{"role": "user", "content": "No, that's all for now. Thank you for your help."}])
    await session.add_items([{"role": "assistant", "content": "You're welcome. Is there anything else I can help you with?"}])
    # At this point, with context_limit=4, everything *before* the earliest of the last 4 turns
    # is summarized into a synthetic pair, and the last 2 turns remain verbatim.
    history = await session.get_items()
    print(f"\n\n[HISTORY_LENGTH AFTER ADD ITEMS]: {len(history)}\n\n")
    print(f"\n\n[HISTORY]: {history}\n\n")

    print(f"\n\n[Using get_items_with_metadata method to get the full history of the session including the metadata for debugging and analysis purposes]\n\n")
    # full_history = await session.get_items_with_metadata()
    # print(f"\n\n[FULL HISTORY]: {full_history}\n\n")
    # print(f"\n\n[FULL HISTORY LENGTH]: {len(full_history)}\n\n")

if __name__ == "__main__":
    asyncio.run(main())
        
    


# Pass `history` into your agent runner / responses call as the conversation context.