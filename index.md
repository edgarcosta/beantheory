### This weekaa
<ul>
{% for talk in site.data.talks.thisweek %}
  <li>
    {{talk['time'] | fmtdatetime}}
    - {{talk['speaker']}}
    {% if talk['desc'] %}
      <br>
      {{ talk['desc'] }}
    {% endif %}
    <br>
    at {{talk['place']}} - {{talk['room']}}
  </li>
  {% endfor %}
</ul>
### Upcoming
<ul>
{% for talk in site.data.talks.upcoming %}
  <li>
    {{talk['time'] | fmtdatetime}}
    - {{talk['speaker']}}
    {% if talk['desc'] %}
      <br>
      {{ talk['desc'] }}
    {% endif %}
    <br>
    at {{talk['place']}} - {{talk['room']}}
  </li>
  {% endfor %}
</ul>
### Past
<ul>
{% for talk in site.data.talks.past %}
  <li>
    {{talk['time'] | fmtdatetime}}
    - {{talk['speaker']}}
    {% if talk['desc'] %}
      <br>
      {{ talk['desc'] }}
    {% endif %}
    <br>
    at {{talk['place']}} - {{talk['room']}}
  </li>
  {% endfor %}
</ul>
