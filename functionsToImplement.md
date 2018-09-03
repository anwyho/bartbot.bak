Functions to Implement
======================

All function stubs are written in Python psudocode. See the [Python 3.5 Typing module](https://docs.python.org/3/library/typing.html) for more information on how to read these stubs.

- [ ] App greeting. [Set it here.](https://developers.facebook.com/docs/messenger-platform/discovery/welcome-screen#set_greeting)

- [ ] Incorporate accessibility emojis (maybe parking emojis too?) and cost/trip

- [ ] Next departure times to arrive before or by arrival time

  ```python
  def departureTimes(orig:Station, arr:Time=None, dest:Union[Station,Direction,Line,Location]=None) -> deps: List[Tuple[Time,Line]]
  ```

  Directions can be either northbound or southbound. Time is BART time, with BART midnight being 2:27 AM.

  <details><summary>Example Queries</summary><p>

  Simple Queries

  - When is the next train from Union City to Bay Fair?
  - What are the next trains out of Dublin? (Dublin/Pleasanton)
  - Can I catch the next Powell to Concord?
  - n concord to gpark

  Advanced Queries

  - Should I run to catch the next Rockridge to W Oakland?
  - What are the next trains to El Cerrito Plaza if I get to Fremont BART by 6pm
  - nconc tmrw 6pm to gpark
  - What barts come at 7am tomorrow from Fremont to Montgomery?
  - When is the first BART from West Dublin Pleasanton to Colma?
  - What is the first train out of Warm Springs?
  - next train from s fremont
    - any/north/northbound/daly city/

  </p></details>

- [ ] Next arrival times at or after departure time or current time

  ```python
  def arrivalTimes(orig:Union[Station,Location], dest:Station, dep:Time=None) -> arrs:List[Tuple[Time,Line]]
  ```

  <details><summary>Example Queries</summary><p>

  Simple Queries

  - What trains get to at SFO from MacArthur next Tuesday at noon?
  - what are the trains that arrive to coliseum by 7p from s fremont
  - When should I get to South San Francisco to get to Richmond by 4p?

  Advanced Queries
  - last bart from embarcadero to dberk
  - s hay by 8pm
    - powell
  - can i get to s fremont from el cerrito by 4 pm?

  </p></details>

- [ ] ETA given an origin, a destination, and a departure time

  ```python
  def eta(orig:Union[Station,Location], dest:Union[Station,Location], dep:Time) -> eta:Time
  ```

  ```python
  def eta(context:Context) -> eta:Time
  ```

  - [ ] Returns in a human-friendly string
    ```python
    def forwardableEta(eta:Time) -> textEta:str
    ```

  <details><summary>Example Queries</summary><p>

  Simple Queries

  - What time will I get to San Bruno?
  - When will I arrive at Powell?
  - eta to rockridge

  Advanced Queries

  - Can I get an eta there?
  - When is my eta?
  - What's my eta?
  - wat time arrive

  </p></details>

- [ ] Cost returned in cents

  ```python
  def cost(orig:Station, dest:Station, type:Ticket='Cash') -> cost:int
  ```

  <details><summary>Example Queries</summary><p>

  - How much is a ride from Rockridge to South Fremont?
  - how much is dberk to powell
  - what does dub to conc cost
  - how expensive is bayfair to colma

  </p></details>

- [ ] Accessibility at station (maybe send an emoji instead)

  ```python
  def accessibility(sta:Station) -> isAccessible:bool
  ```

  <details><summary>Example Queries</summary><p>

  - Is Colma wheelchair accessible?
  - accessibility at bayfair
  - montgomery accessibility

  </p></details>

- [ ] Parking at station

  ```python
  def parking(sta:Station) -> hasParking:bool
  ```

  <details><summary>Example Queries</summary><p>

  - Does Union City have parking?
  - parking at s fremont
  - ashby parking

  </p></details>

- [ ] Delays along a route - maybe make this a periodically run function that broadcasts to people who recently looked up trips on that route in the past 30min? See the [Messenger Broadcasting](https://developers.facebook.com/docs/messenger-platform/send-messages/broadcast-messages/) feature.

  ```python
  def delays(orig:Station) -> delays:List[String]
  ```

  <details><summary>Example Queries</summary><p>

  - are there any delays?
  - delays

  </p></details>

- [ ] Send feedback

  ```python
  def feedback(msg:str) -> confirmationAndEmail:str
  ```

  <details><summary>Example Queries</summary><p>

  - feedback
  - suggestions

  </p></details>

- [ ] Support me through a donation at my [PayPal.me](https://www.paypal.me/anwyho)

  <details><summary>Example Queries</summary><p>

  - how can i support
  - how can i donate
  - donation

  </p></details>

Future Features
---------------

- [ ] Nearest station

  ```python
  def nearestStation(loc:Location) -> sta:Station
  ```

- [ ] Weather, station info, around the station

  ```python
  def stationInfo(sta:Station) -> stationInfo:str
  ```

  <details><summary>Example Queries</summary><p>

  <!-- Implment this soon -->

  - What's the weather around downtown berkeley tomorrow?
  - Will it rain around sfo on tuesday?
  - weather at d city

  </p></details>

- [ ] Weekly poll?

  ```python
  def weeklyPollSubmission(response:int) -> confirmation:bool
  ```

  <details><summary>Example Queries</summary><p>

  <!-- Implment this soon -->

  - q1
  - q2
  - q3
  - q4
  - q5
  - q6
  - q7
  - q8
  - q9
  - q10

  </p></details>

- [ ] Fun things for BART ride (maybe XKCD comics?)

  ```python
  def entertainMe() -> stuff:Union[Image,String,Url]
  ```

  <details><summary>Example Queries</summary><p>

  <!-- Implment this soon -->

  - q1
  - q2
  - q3

  </p></details>

- [ ] Report something to BART police at station

  ```python
  def reportEventToPolice(sta:Station=None) -> confirmationAndInfo:str
  ```

  <details><summary>Example Queries</summary><p>

  <!-- Implment this soon -->

  - q1
  - q2
  - q3

  </p></details>

- [ ] Set up Uber or Lyft

  ```python
  def uberLyftLink(setUpUber:bool, dest:Station, arr:Time) -> handle:Url
  ```

  <details><summary>Example Queries</summary><p>

  <!-- Implment this soon -->

  - q1
  - q2
  - q3

  </p></details>

- [ ] Reminders (not exact implementation)
  - [ ] Request [subscription messaging](https://www.facebook.com/bartbotable/settings/?tab=messenger_platform)
  - [ ] Ask to set up reminder to transfer or for arrival (Send callback on positive?)

    ```python
    def reminder() -> callback:Callable[[bool, bool],Context]
    ```

    <details><summary>Example Queries</summary><p>

    <!-- Implment this soon -->

    - q1
    - q2
    - q3

    </p></details>

    Allow user to silence this feature if both are false (after three times?)

  - [ ] Request reminder to transefer and/or get off (remind user that this is a beta feature)

    ```python
    def requestReminders(transfer:bool, arr:bool, context:Context) -> confirmSetup:bool
    ```

    <details><summary>Example Queries</summary><p>

    <!-- Implment this soon -->

    - q1
    - q2
    - q3

    </p></details>

- [ ] Nearest BART station with some amount of error (thinking about SF stations that are really close to each other)

  ```python
  def nearestStation(loc:Location) -> stas:Tuple[dist,Station]
  ```

  <details><summary>Example Queries</summary><p>

  <!-- Implment this soon -->

  - q1
  - q2
  - q3

  </p></details>

- [ ] Support holiday schedules

  <details><summary>Example Queries</summary><p>

  <!-- Implment this soon -->

  - q1
  - q2
  - q3

  </p></details>

- [ ] Friends also using bartbot

- [ ] Commute capabilities
  - [ ] Name commutes
  - [ ] Set up reminders to catch commutes
  - [ ] Ability to change reminder time and delete commutes
  - [ ] Limit to only 5 commutes per user?
  - [ ] After three of the same queries for station arrivals, suggest making a Commute

  <details><summary>Example Queries</summary><p>

  <!-- Implment this soon -->

  - q1
  - q2
  - q3

  </p></details>

- [ ] Implement [Google speech-to-text](https://cloud.google.com/speech-to-text/)

- [ ] Implement a fuzzy search for station names
  - [ ] Change this for speech-to-text (phonetic fuzzy search)

- [ ] For Wit.ai, implement renaming intent
- [ ] Implement ability to rename stations or nickname stations
- [ ] [Messenger Picture Code](https://developers.facebook.com/docs/messenger-platform/reference/messenger-code-api)