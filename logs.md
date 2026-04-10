### dev logging for MCP server creation
## Monday the 30th. Configured arista OS, GNS3 is a piece of shit and wont let me ssh externally. 
* switch to container lab as its just better. Container lab works with my IP alot better. everything just works.
* container lab set up to use arista OS.
* Too few interfaces added a secodn router so I can make a few more connected interfaces for things later.
## Wednesday the 1st. 
* Created the MCP server and some basic tools, just read device info and interfaces. Created tool_test so test those starter tools.
* Missed around with claude, want to run this all locally so I dont have to pay for jew api. 
* cant figure out how to make claude use my MCP server will do another day.
## Monday the 5th
* Figured out how to run with ollama to make it all local. Claude code is running without charging me. 
* Created a few more tools, get routes, get running config, configure interface, add static route. 
* Tested that those tools work
* model really hates them does not output properly, must add input validation.
## Thursday the 9th
* added input validation to almost all tools
* runs alot better but still having some tool use issues, qwen requires really specific formatting to get it right.
* Still need to improve input formatting and validation
## Friday the 10th
* input validation is improved, everything works pretty well now, few errors and prompting is still semi specific but its consistent now, you just need to add the word executate to every prompt then it works fine.
* Record video and create write up still to do.
  