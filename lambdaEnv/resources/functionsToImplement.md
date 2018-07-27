// Next departure times to arrive before or by arrival time
deps:{Time} <- orig:Station, [ arr:Time ], [ dest:Station | dir:Direction 
                                           | line:Station ];
                                           
Direction := 'N' | 'S';
Time := 

// Next arrival times at or after departure time or current time
arrs:{Time} <- orig:Station, dest:Station, [ dep:Time ];


eta:Time <- ( orig:Station, dest:Station, dep:Time ) | context:Context 
          | ( loc:Location, dest:Station, dep:Time );
// ETA in forwardable string
forwardEta:str <- eta:Time;

// Cost returned in cents
cost:int <- orig:Station, dest:Station, [ adult:bool ];

accessibility:bool <- sta:Station;

parking:bool <- sta:Station;

delays:{str} <- orig:Station, [ dest:Station ];

// Accepting feedback
responseAndEmail:str <- feedback:str;


// FUTURE FEATURES

// Weather, Station Info, Around the Station
stationInfo{str} <- sta:Station;

// Weekly Poll
confirmation:str <- weeklyPollResponse:int;

// Fun things for BART (maybe XKCD comics?)
stuff{object} <- passTime:bool;

// Report something to BART police?
confirmationAndInfo:str <- reportEventToPolice:bool;

// Set up Uber or Lyft? 
rideLink:URL <- setUpUber:bool, dest:Station, arr:Time;

// Request to send ETA to friend, message friend through Bartbot
// Ask friend if they want to acknowledge, if yes, relay acknowledgement
// Simultaneously do some sharing for Bartbot!