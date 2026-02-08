# Creating Custom MCP Tools

Extend MCP for Unity with project-specific tools using C# attributes and reflection.

## Quick Start

### 1. Create Tool Handler

Place in any `Editor/` folder. Must be static class with `[McpForUnityTool]` attribute and `HandleCommand(JObject)` method.

```csharp
using Newtonsoft.Json.Linq;
using MCPForUnity.Editor.Helpers;
using MCPForUnity.Editor.Tools;

namespace MyProject.Editor.CustomTools
{
    [McpForUnityTool("my_custom_tool")]
    public static class MyCustomTool
    {
        public class Parameters
        {
            [ToolParameter("Value to process")]
            public string param1 { get; set; }

            [ToolParameter("Optional integer payload", Required = false)]
            public int? param2 { get; set; }
        }

        public static object HandleCommand(JObject @params)
        {
            var parameters = @params.ToObject<Parameters>();
            if (string.IsNullOrEmpty(parameters.param1))
                return new ErrorResponse("param1 is required");

            // Do work...
            return new SuccessResponse("Done!", new { parameters.param1, parameters.param2 });
        }
    }
}
```

### 2. Refresh MCP Client

Disconnect and reconnect to the MCP server. Some clients need full reconfiguration.

### 3. Discovery

```bash
unity-mcp tool list
unity-mcp custom_tool list
```

Or read `mcpforunity://custom-tools` resource.

## Long-Running (Polled) Tools

For operations like test runs, lightmap bakes, or builds:

```csharp
[McpForUnityTool("bake_lightmaps", Description = "Async lightmap bake",
    RequiresPolling = true, PollAction = "status")]
public static class BakeLightmaps
{
    public static object HandleCommand(JObject @params)
    {
        // Start work...
        McpJobStateStore.SaveState("bake_lightmaps", new { lastStatus = "in_progress", progress = 0f });
        return new PendingResponse("Starting bake", 0.5);
    }

    public static object Status(JObject _)
    {
        var state = McpJobStateStore.LoadState<MyState>("bake_lightmaps");
        if (state.lastStatus == "completed")
            return new { _mcp_status = "complete", message = "Done", data = state };
        return new PendingResponse($"Baking... {state.progress:P0}", 0.5, state);
    }
}
```

**Key concepts:**
- Return `PendingResponse` with poll interval (0.1-5s, clamped)
- `_mcp_status`: `"pending"` | `"complete"` | `"error"`
- Use `McpJobStateStore` for state persistence across domain reloads
- Timeout: 10 minutes
- PollAction string is case-sensitive — match exactly in HandleCommand
