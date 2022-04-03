from flask import Blueprint, render_template, request

from functions import get_swim_times, event_id_to_event, event_id_to_title
from website.forms import TimeForm

time_routes = Blueprint('time_routes', __name__, template_folder='templates')


@time_routes.route('/', methods=('GET', 'POST'))
def times():
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        event_id = request.form["event"]
        source = request.args.get('source')
        names = name.split()
        time_data = get_swim_times(names[0], names[1], event_id_to_event[gender][event_id])
        if source == "best":
            time = time_data['formatted_best_time']
            text = f"{name}'s Best Time in the {event_id_to_title[gender][event_id]} is a {time}"
        elif source == "estim":
            time = time_data['formatted_estimate']
            text = f"{name}'s Estimated Next Time in the {event_id_to_title[gender][event_id]} is a {time}"
        elif source == "all":
            time = time_data['formatted_times']
            text = f"{name}'s Times in the {event_id_to_title[gender][event_id]} are {time}"
        else:
            text = "Error fetching data!"

        return render_template('times/get_times.html', text=text)
    else:
        return render_template('times/times.html')


@time_routes.route('/best/')
def best_times():
    form = TimeForm()
    return render_template('times/best.html', form=form)


@time_routes.route('/estim/')
def estim_times():
    form = TimeForm()
    return render_template('times/estim.html', form=form)


@time_routes.route('/all/')
def all_times():
    form = TimeForm()
    return render_template('times/all.html', form=form)
