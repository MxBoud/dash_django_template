# dash_app.py
from dash import Dash, dcc, html, Input, Output, State, ctx
from setup_django import django
from events.models import Event  # Import your Django model



app = Dash(__name__)

# Dash Layout
app.layout = html.Div([
    html.H1("Event Data Collection"),
    html.Div([
        html.Label("Title"),
        dcc.Input(id='title', type='text', placeholder="Event Title"),
        html.Label("Date"),
        dcc.Input(id='date', type='text', placeholder="Event Date"),
        html.Label("Location"),
        dcc.Input(id='location', type='text', placeholder="Event Location"),
        html.Label("Description"),
        dcc.Textarea(id='description', placeholder="Event Description"),
        html.Button('Submit', id='submit', n_clicks=0),
    ]),
    html.Div(id='feedback', style={'marginTop': '20px'}),
    html.Hr(),
    html.Div([
        html.H2("Stored Events"),
        html.Ul(id='event-list')
    ])
])

# Dash Callbacks
@app.callback(
    Output('feedback', 'children'),
    Output('event-list', 'children'),
    Input('submit', 'n_clicks'),
    State('title', 'value'),
    State('date', 'value'),
    State('location', 'value'),
    State('description', 'value')
)
def submit_event(n_clicks, title, date, location, description):
    feedback = ""
    if ctx.triggered_id == 'submit' and n_clicks > 0:
        # Save event using Django ORM
        if not (title and date and location):
            feedback =  "Error: Please provide Title, Date, and Location."
        
        event = Event.objects.create(title=title, date=date, location=location, description=description)
        feedback =  f"Event '{event.title}' successfully added!"
    events = Event.objects.all()
    events_list = [html.Li(f"{event.date} - {event.title} ({event.location})") for event in events]
    return feedback, events_list



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
