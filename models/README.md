# 🤖 Model & Provider Capability Profiles (`models/`)

Defines context windows, tool calling capabilities, modality support, and latency/cost classes for routing skills to optimal foundation models.

---

## 📊 Model Capability Matrix

| Provider | Model ID | Context Window | Vision | Tool Calling | Structured Output | Reasoning Class |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Anthropic** | `claude-3-5-sonnet` | 200k | ✅ | ✅ | ✅ | Frontier |
| **OpenAI** | `gpt-4o` | 128k | ✅ | ✅ | ✅ | Frontier |
| **Google** | `gemini-1-5-pro` | 2M | ✅ | ✅ | ✅ | Frontier Long-Context |
| **Meta** | `llama-3-3-70b` | 128k | ❌ | ✅ | ✅ | High-Performance OSS |
| **Local** | `qwen2-5-coder-32b` | 32k | ❌ | ✅ | ✅ | Local Sovereign Code |
