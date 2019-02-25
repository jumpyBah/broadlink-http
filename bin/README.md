# HTTP server for Broadlink RM

 
## Installation

Need to install required Python modules using  
`sudo pip install broadlink`
`sudo pip install yaml`

## Configuration
All configurable parameters are present in `config.yaml` file. 
Without parameters the default is the section `broadlink`.

### Multiple devices configuration

You can enter the configuration of multiple devices and select them using the -d option.

e.g. python bhrc.py -d sala
