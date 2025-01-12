import io
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, ctx
from dash.dependencies import ALL
from setup_django import django
from events.models import Event  # Import your Django model
from flask import send_file
import matplotlib.pyplot as plt


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
        dcc.Dropdown(
            id='event-dropdown',
            placeholder="Select an Event to Export",
            options=[],  # Will be dynamically populated
        ),
        html.Button('Download Event Details', id='download-btn', n_clicks=0),
        dcc.Download(id='download-event')
    ]),
    html.Div(id='event-list-container', style={'marginTop': '20px'})
])

# Callback to handle event submission and list update
@app.callback(
    Output('feedback', 'children'),
    Output('event-list-container', 'children'),
    Output('event-dropdown', 'options'),
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
            feedback = "Error: Please provide Title, Date, and Location."
        else:
            event = Event.objects.create(title=title, date=date, location=location, description=description)
            feedback = f"Event '{event.title}' successfully added!"

    # Retrieve all events from the database
    events = Event.objects.all()
    events_list = [html.Li(f"{event.date} - {event.title} ({event.location})") for event in events]
    dropdown_options = [{'label': f"{event.title} - {event.date}", 'value': event.id} for event in events]

    return feedback, html.Ul(events_list), dropdown_options


@app.callback(
    Output('download-event', 'data'),
    Input('download-btn', 'n_clicks'),
    State('event-dropdown', 'value')
)
def download_event_details(n_clicks, event_id):
    if n_clicks > 0 and event_id:
        # Retrieve the selected event from the database
        event = Event.objects.get(id=event_id)
        
        # Create a DataFrame for the event details
        data = {
            "Field": ["Title", "Date", "Location", "Description"],
            "Value": [event.title, event.date, event.location, event.description]
        }
        df = pd.DataFrame(data)

        # Generate a sine wave plot
        plt.figure(figsize=(6, 4))
        x = [i / 10.0 for i in range(100)]
        y = [10 * (i ** 0.5) for i in x]
        plt.plot(x, y, label="Sine Wave", color="blue")
        plt.title("Sine Wave Plot")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()

        # Save the plot to an in-memory buffer
        plot_buffer = io.BytesIO()
        plt.savefig(plot_buffer, format='png')
        plt.close()
        plot_buffer.seek(0)

        # Convert the DataFrame to an Excel file in memory
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write the DataFrame to the first sheet
            df.to_excel(writer, index=False, sheet_name="Event Details")

            # Access the workbook and worksheet
            workbook = writer.book
            worksheet = workbook.add_worksheet("Sine Wave Plot")
            writer.sheets["Sine Wave Plot"] = worksheet

            # Insert the plot image into the second sheet
            worksheet.insert_image('C10', 'sine_wave.png', {'image_data': plot_buffer})
        
        buffer.seek(0)

        # Use Dash's native dcc.Download
        return dcc.send_bytes(buffer.getvalue(), filename=f"Event_{event.title}.xlsx")
    return None


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
