# Bespoken TODO

## Potential Tools to Add

### Environment Variables Tool
- Read environment variables (`env.get("PATH")`)
- List all environment variables (`env.list()`)
- Check if specific env vars are set (`env.check("NODE_ENV")`)
- Could be useful for debugging deployment issues, checking configs, etc.
- Example: "What's my current PATH?" -> tool reads and formats env vars

## Completed Features
- ✅ Tab completion with prompt_toolkit
- ✅ Consistent UI padding system
- ✅ Command execution tools (GitTool, NpmTool, PythonTool)
- ✅ Trust system for tools

## In Progress
- @ symbol for file path autocompletion
- / slash commands for actions
- User-configurable shortcuts

## Ideas for Later
- Editor integration for @selection references
- Git integration improvements
- More specialized tools (Docker, AWS, etc.)