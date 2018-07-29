Functions to Implement
======================

All function stubs are written in Python psudocode. See the [Python 3.5 Typing module](https://docs.python.org/3/library/typing.html) for more information on how to read these stubs.

- [ ] Next departure times to arrive before or by arrival time

  ```python
  def departureTimes(orig:Station, arr:Time=None, dest:Union[Station,Direction,Line,Location]=None) -> deps: List[Tuple[Time,Line]]
  ```

  Directions can be either northbound or southbound. Time is BART time, with BART midnight being 2:27 AM.

- [ ] Next arrival times at or after departure time or current time

  ```python
  def arrivalTimes(orig:Union[Station,Location], dest:Station, dep:Time=None) -> arrs:List[Tuple[Time,Line]]
  ```

- [ ] ETA given an origin, a destination, and a departure time

  ```python
  def eta(orig:Union[Station,Location], dest:Union[Station,Location], dep:Time) -> eta:Time
  ```

  ```python
  def eta(context:Context) -> eta:Time
  ```

  - [ ] Returns in a forwarding-friendly string
    ```python
    def forwardableEta(eta:Time) -> textEta:str
    ```

- [ ] Cost returned in cents

  ```python
  def cost(orig:Station, dest:Station, type:Ticket='Cash') -> cost:int
  ```

- [ ] Accessibility at station

  ```python
  def accessibility(sta:Station) -> isAccessible:bool
  ```

- [ ] Parking at station

  ```python
  def parking(sta:Station) -> hasParking:bool
  ```

- [ ] Delays along a route - maybe make this a periodically run function that broadcasts to people who recently looked up trips on that route in the past 30min? See the [Messenger Broadcasting](https://developers.facebook.com/docs/messenger-platform/send-messages/broadcast-messages/) feature.

  ```python
  def delays(orig:Station) -> delays:List[String]
  ```

- [ ] Send feedback

  ```python
  def feedback(msg:str) -> confirmationAndEmail:str
  ```

- [ ] Support me through a donation at my [PayPal.me](https://www.paypal.me/anwyho)

Future Features
---------------

- [ ] Weather, station info, around the station

  ```python
  def stationInfo(sta:Station) -> stationInfo:str
  ```

- [ ] Weekly poll?

  ```python
  def weeklyPollSubmission(response:int) -> confirmation:bool
  ```

- [ ] Fun things for BART ride (maybe XKCD comics?)

  ```python
  def entertainMe() -> stuff:Union[Image,String,Url]
  ```

- [ ] Report something to BART police at station

  ```python
  def reportEventToPolice(sta:Station=None) -> confirmationAndInfo:str
  ```

- [ ] Set up Uber or Lyft

  ```python
  def uberLyftLink(setUpUber:bool, dest:Station, arr:Time) -> handle:Url
  ```

- [ ] Reminders (not exact implementation)
  - [ ] Ask to set up reminder to transfer or for arrival (Send callback on positive?)

    ```python
    def reminder() -> callback:Callable[[bool, bool],Context]
    ```

    Allow user to silence this feature if both are false (after three times?)

  - [ ] Request reminder to transefer and/or get off (remind user that this is a beta feature)

    ```python
    def requestReminders(transfer:bool, arr:bool, context:Context) -> confirmSetup:bool
    ```

- [ ] Nearest BART station with some amount of error (thinking about SF stations that are really close to each other)

  ```python
  def nearestStation(loc:Location) -> stas:Tuple[dist,Station]
  ```

- [ ] Support holiday schedules

- [ ] Commute capabilities
  - [ ] Name commutes
  - [ ] Set up reminders to catch commutes
  - [ ] Ability to change reminder time and delete commutes
  - [ ] Limit to only 5 commutes per user?
  - [ ] After three of the same queries for station arrivals, suggest making a Commute
