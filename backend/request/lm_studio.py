import json


class LMStudioRequest:
    def __init__(self, body, tools=None, structured_output=None):
        self.body = body
        self.tools = tools
        self.structured_output = structured_output

    def xml_format(self):
        f = to_xml_format(self)
        return f

def to_xml_format(request: LMStudioRequest):
    isBodyList = isinstance(request.body, list)
    if isBodyList or request.tools is not None or request.structured_output is not None:
        s = ["<request>"]
        if isBodyList:
            for content in request.body:
                role = content.get("role")
                value = content.get("content")
                if isinstance(value, str):
                    s+=[f"""
<{role}>
{value}
</{role}>
""".strip(),]
                elif isinstance(value, list):
                    s += ["<user>"]
                    for content_obj in value:
                        t = content_obj.get("type")
                        t_value = content_obj.get("text")
                        s += [f"""
<{t}>
{t_value}
</{t}>
""".strip(),]
                    s += ["</user>"]
        else:
            s += [f"""
<user>
{request.body}
</user>
            """.strip(), ]


        if request.tools is not None:
            s += ["""
<system>
If you need to use a tool to answer please use the defined tools. 
Assuming the tools is 
```
{"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather in a given location","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The city and state, e.g. San Francisco, CA"},"unit":{"type":"string","enum":["celsius","fahrenheit"]}},"required":["location"]}}}]}
```
When you do use a tool your output should like
``` 
{"tool_calls":[{"type":"function","function":{"name":"get_current_weather","arguments":"{\n\"location\": \"Boston, MA\"\n}"}}]}
``` 
You must answer by exactly following the provided instructions. Do not add any additional comments or explanations.
Do not add "Here is..." or anything like that.

Act like a script, you are given an optional input and the instructions to perform, you answer with the output of the requested task.

Please only output plain json when using tools.
<tool>
            """.strip(), json.dumps(request.tools, ensure_ascii=False, indent=4), "</tool>\n</system>" ]

        if request.structured_output is not None:
            s += ["""
<system>
## OUTPUT FORMAT: 
- Be sure that all outputs are JSON-compatible. 
- Output in JSON format and ensure that the JSON Schema is followed. 
- Do not include any preface or any other comments. 
- Do NOT use markup. 
- The output MUST be plain JSON with no other formatting or markup. 
- Include every part of the JSON FORMAT, even if a response is missing. 
- The Output MUST begin with { and the Output MUST end with }

### JSON Schema:
``` json
""".strip(),
                  json.dumps(request.structured_output["json_schema"], ensure_ascii=False, indent=4), """
``` 
</system>
""".strip()]


        s += ["</request>"]
        return "\n".join(s)

    elif isinstance(request.body, str):
        return request.body