# ESC204_PraxisIII_The-wandering_sheep

Design considerations
The wandering sheep project implemented the "Improving GSM-based sheep tracking: Using a cluster-based multi-hop approach" paper to develop a cost efficient but accurate sheep tracking system for residents in Rosedale, Mthatha, South Africa.


## Electrical requirements
1. Go to /Follower Sheep(Wireless Transceiver), download the adafruit library zip.
2. Add it to the arduino libraries file, open files->examples->adafruit blue fruitLE nF51->blueart_cmdmode.
3. Uncomment the software UART in the code, comment the default SPI code.
4. Download the Blue Connect mobile phone app, connect it to the bluefruit device.
5. Upload to the board and open the serial monitor.
6. If upload failed, check the serial port, make sure it's the arduino UNO port.

## Collar design requirements
1. The CAD model files of the collar design is in /Physical Collar.

## Back end requirements
1. The back end database with an example used in the demo video is in /Backend Database.

## PM documentations and the final deliverables
1. The PM artefacts are in /Team Process (formal checkin documents), and /Housekeeping.
2. There are two main deliverables, the Proposal and the Pitch, relavent documents are in /Design Milestones.
