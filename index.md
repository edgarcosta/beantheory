{% include talks_block.html title="This week" talks=site.data.talks.thisweek %}
{% include talks_block.html title="Upcoming" talks=site.data.talks.upcoming %}
### [Previous](./previous.html)

#### Currently covering:
<ul>
{% for s in site.data.talks.seminars %}
  <li>
   <a href="{{s.url}}">{{s.name}}</a>
  {% if s.errors != ''%}
    {% include cross.html title=s.errors %}
  {% endif %}
  (<a href="#" id="{{s.label}}" class="button-toggle" >Hide</a>)
  </li>
{% endfor %}
</ul>


