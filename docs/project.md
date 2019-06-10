#Ein Ferngesteuertes Auto fährt von allein!
##Das RC Auto vorbereiten
Das Ferngesteuerte Auto *sollte* ein 1:10 Modellauto sein. Es existieren auch Ferngesteuerte Autos im Spielzeug Segment, allerdings ist deren
Motor **kein Servomotor**. Um ein RC Auto mit einem Raspberry Pi möglichst einfach zu verbinden, empfiehlt sich ein Servomotor.
So ein Spielzeug Auto hat 4Pins mit einem servo-ähnlichen Verhalten. Es wäre prinzipiell möglich auch das mit einem RaspberryPI
zu verbinden, allerdings ist so etwas dann eher im Elektrotechnik Fachgebiet.

###Der Servomotor
Der Servomotor eines Modellautos hat 3 Pins. Die 3 Pins sind

* Versorgungspannung
* Masse
* Signal/PWM

Wir haben einen **SunFounder PCA9685** als 12 Bit PWM Servo Driver verwendet. Vom Raspberry Pi müssen wir nun 4 Pins an den Servo Driver anschließen. Die 5V vom Pi an z.B Pin 2 muss an den VCC (+) Pol des Drivers angeschlossen werden.
Dann vom Pi die Masse z.B Pin 6 muss an die Masse (GND) vom Driver angeschlossen werden. Die Daten müssen aber auch vom Pi in den Motor fließen. Dafür verwenden wir einen I^2C Bus. Diesen Bus verwenden wir über die beiden Pins
SDL (Serial Data) und SCL (Serial Clock). Der SDl schickt die Daten und der SCL setzt den Taktimpuls. Der SDL hat eine 10Bit Adressierung.
Sowohl der Pi als auch der Driver haben einen SDL & SCL Anschluss Pin, die haben wir nun auch verbunden.
Als letzten Schritt muss der Motor noch mit dem Servotreiber verbunden werden. Ein echtes Modellauto hat immer einen wie oben beschriebenen 3 Pin Anschluss. Der Servo hat 3x16 Reihen Pins zur freien Verfügung, die jeweils
in PWM, V+ und GND (Masse) aufgeteilt sind. Der 3er Pin Block vom Motor muss nun einfach an eine dieser 16 Reihen eingesteckt werden.
Soweit fertig mit dem Verbinden.


###Kameramodul und Webserver

* Über die IP-Adresse *192.168.2.125  und den Port 8887* kann ein Webinterface aufgerufen werden, über dieses kann das Auto später bewegt werden und die Kamera eingesehen werden.
* Die Information (Vor, Zurück, Links und Recht) wird mittels JSON an den Webserver der vom Pi gehostet wird geschickt. Das Pi wartet darauf Daten zu bekommen, um anschließend das richtige PWM Signal zu senden.

##Abstraktionsebenen
* [Abstraktionsebene 1 - Grobe Gesamtübersicht](Ebene_1.pdf)
* [Abstraktionsebene 2 - Sicht Laptop - Webserver](Ebene_2_Laptop.pdf)
* [Abstraktionsebene 2 - Sicht RaspberryPi - Motor](Ebene_2_Raspi.pdf)
* [Abstraktionsebene 3 - Neuronales Netz](cnn_donkeycar2.pdf)

##Neuronales Netz
Wir haben ein wenig mit den verschiedenen Layern herumgespielt und sind zu einem recht guten Ergebnis gekommen. Diese Netze wurden bisher nur auf einem
Online-Simulator getestet, aber es zeigt, dass eine Strecke und vor allem die Mittellinie erkannt werden.

###Fast ohne Ausreißer:

`Gutes Netz:
x = Convolution2D(24, (5, 5), strides=(2, 2), activation='relu')(x)  
x = Convolution2D(32, (5, 5), strides=(2, 2), activation='relu')(x)  
x = Convolution2D(64, (5, 5), strides=(2, 2), activation='relu')(x)
x = Convolution2D(64, (3, 3), strides=(2, 2), activation='relu')(x)  
x = Convolution2D(64, (3, 3), strides=(1, 1), activation='sigmoid’)(x)  
x = Flatten(name='flattened')(x)
x = Dense(300, activation='relu')(x)  
x = Dense(20, activation='relu')(x)
`
***
###Fährt im Kreis:

`Schlechtes Netz:
x = Convolution2D(filters=24, kernel_size=(5, 5), strides=(2, 2), activation='relu')(x)
x = Convolution2D(filters=32, kernel_size=(5, 5), strides=(2, 2), activation='relu')(x)
x = Convolution2D(filters=64, kernel_size=(5, 5), strides=(2, 2), activation='relu')(x)
x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(2, 2), activation='relu')(x)
x = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu')(x)
x = Flatten(name='flattened')(x)
x = Dense(units=100, activation='linear')(x)
x = Dropout(rate=.1)(x)
x = Dense(units=50, activation='linear')(x)
x = Dropout(rate=.1)(x)
angle_out = Dense(units=1, activation='linear', name='angle_out')(x)
throttle_out = Dense(units=1, activation='linear', name='throttle_out')(x)
model = Model(inputs=[img_in], outputs=[angle_out, throttle_out])
model.compile(optimizer='adam',loss={'angle_out': 'mean_squared_error','throttle_out': 'mean_squared_error'},loss_weights={'angle_out': 0.5, 'throttle_out': .5})`

###Fährt im Kreis
<iframe width="560" height="315" src="https://www.youtube.com/embed/lWnZAFxccfs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Fährt !
<iframe width="560" height="315" src="https://www.youtube.com/embed/VwHTCMuq3xs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
