<!-- templates/statuses/status_form.html -->
{% extends "base.html" %}
{% load django_bootstrap5 %}

{% block content %}
  <h1 class="my-4">{% if form.instance.pk %}Редактировать статус{% else %}Новый статус{% endif %}</h1>
  
  <form method="post">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% bootstrap_button button_type="submit" content="Создать" button_class="btn-primary" %}
    <a href="{% url 'status_list' %}" class="btn btn-secondary">Отмена</a>
  </form>
{% endblock %}
