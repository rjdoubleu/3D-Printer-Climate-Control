# 3D-Printer-Climate-Control
My project for embedded systems (Spring 2019) was to create a 3D printer enclosure with climate control. Although this project did not turn out as expected I still learned a lot about embedded system programming.

## Project Proposal
The Project Proposal can be accessed at [this link](https://docs.google.com/document/d/1nhE-VeoW2xHojhICf00JVar8DhTzB7k-zKPyljFL4bU/edit?usp=sharing). The general idea was to address several safety and efficieny issues with 3D printing by creating an enclosure with climate control.

## Embedded System Development Reflections
### Software and Circuts
This project utilized a RPi and Arduino to manage the various systems at play. Relays, a buck converter and IoT switch were implemented to manage the wide range of voltages across the components. Wirring gauge was accounted for in properly powering various units as well as safety procedures in handling high voltage systems. One key goal missed in the project was integrating the embedded software with the OctoPi GUI by deploying it as a pluggin. The software and GUI functioned properly seperately but the plugin architecture was never achieved (discussed in detail below). [*climateTest.py*](https://github.com/rjdoubleu/3D-Printer-Climate-Control/blob/master/climateTest.py) and [*gasSensors.ino*](https://github.com/rjdoubleu/3D-Printer-Climate-Control/blob/master/gasSensors.ino) are the software files for the RPi and Arduino respectively.

### Hardware
In total there were 8 individual components comprised of a space heater, two smoke detectors, two temperature and humidity sensors, two bypass valves, and a dehumidifier. This large feature set was incredibly challenging to implement successfully in addition to the design of 5 custom 3d printed and designed parts including valve stems, the dehumidifier enclosure, the PSU relocation bracket, and the charcoal filter mounting tray. In retrospect, implementing all of this custom design for a project lacking a prexisting guidline or tutorial was an overextension of my abilities under the circumstances. Nonetheless, I learned a massive amount in regards to mechatronics.

## Project Image Reel

## Software

<img src="https://github.com/rjdoubleu/3D-Printer-Climate-Control/blob/master/Software%20Images/Sample%20Output.PNG">

<img src="https://github.com/rjdoubleu/3D-Printer-Climate-Control/blob/master/Software%20Images/octoPrint%20Screen.PNG">


## Components


## Custom Hardware
All custom hardware was designed in Tinkercad.

<img src="https://github.com/rjdoubleu/3D-Printer-Climate-Control/blob/master/Custom%203D%20Parts/basePlate.png" width="200">

<img src="https://github.com/rjdoubleu/3D-Printer-Climate-Control/blob/master/Custom%203D%20Parts/before.PNG" width="200">

<img src="https://github.com/rjdoubleu/3D-Printer-Climate-Control/blob/master/Custom%203D%20Parts/dehumEnc.PNG" width="200">

<img src="https://github.com/rjdoubleu/3D-Printer-Climate-Control/blob/master/Custom%203D%20Parts/fan%20fitment%20p2.PNG" width="200">

<img src="https://github.com/rjdoubleu/3D-Printer-Climate-Control/blob/master/Custom%203D%20Parts/valveStems.png" width="200">
