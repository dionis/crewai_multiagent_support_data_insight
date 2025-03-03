
## Notes

## Human Input

- With Gemini there are a Big Issue because was set human_input the crewai request send the request as example:
  - ``POST Request Sent from LiteLLM:
curl -X POST \
https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=<GEMINI_API_KEY> \
-H 'Content-Type: *****' \
-d '{'contents': [], 'system_instruction': {'parts': [{'text': 'Determine if the following feedback indicates that the user is satisfied or if further changes are needed. Respond with \'True\' if further changes are needed, or \'False\' if the user is satisfied. **Important** Do not include any additional commentary outside of your \'True\' or \'False\' response.\n\nFeedback: "looks good"'}]}, 'generationConfig': {'temperature': 0.7, 'stop_sequences': ['\nObservation:']}}'

``

  there are an issue because send an empty array [] in code. In document [Resolving Gemini's Bad Request Error When Passing.pdf](/Resolving Gemini's Bad Request Error When Passing.pdf)
  there are some tips for fixed.
  
 
