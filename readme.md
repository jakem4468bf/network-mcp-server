### MCP server for local LLM's to control and configure arista (and likely any vendor) network devices.

## Lab ENV setup

* Download container lab from [Container Lab](https://containerlab.dev/install/)
* Download arista ceos image from [Arista](https://www.arista.com/en/support/software-download)
* import arista ceos (rename version to whatever version you download)

`docker import cEOS64-lab-4.32.0F.tar.xz ceos:4.32.0F`

* After import check images using `docker images`
* Create lab using provided topology file `containerlab deploy -t network_lab.yaml`
* Access CLI using `sudo docker exec -it r1 Cli`
* Configure SSH on router 

```
enable
configure terminal
username admin privilege 15 secret admin123
management api http-commands
   no shutdown
exit
write memory
```

* You can now ssh into the router from you host machine using `ssh admin@localhost -p 2201`

## MCP server setup

* Open virtual envoirnment using `venv\Scripts\activate`
* Install dependencies using `pip install -r requirements.txt`
* Run the server using `python server.py`

## Agent setup

* Download ollama from [Ollama](https://ollama.com/)
* Download qwen3-coder:30b model using `ollama pull qwen3-coder:30b` (or any model you would like)
* Launch claude code using `ollama launch claude --model qwen3-coder:30b -- --mcp-config "C:\Users\Jake\network-mcp-server\mcp_config.json"`
* Ask away

## Tools are located in server.py file, netmiko is used for SSH connections and sending commands to the device. If you run into issues, there are tester files in the repo to test tools individually.