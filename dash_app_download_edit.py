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
    html.H1("Event Data Management"),
    html.Div([
        html.H2("Add or Edit Event"),
        html.Label("Select Event to Edit"),
        dcc.Dropdown(id='event-select', placeholder="Select an Event", options=[]),
        html.Label("Title"),
        dcc.Input(id='edit-title', type='text', placeholder="Event Title"),
        html.Label("Date"),
        dcc.Input(id='edit-date', type='text', placeholder="Event Date"),
        html.Label("Location"),
        dcc.Input(id='edit-location', type='text', placeholder="Event Location"),
        html.Label("Description"),
        dcc.Textarea(id='edit-description', placeholder="Event Description"),
        html.Button('Save Changes', id='save-event-btn', n_clicks=0),
        html.Button('Add New Event', id='add-new-event-btn', n_clicks=0),
        html.Button('Download Event Details', id='download-btn', n_clicks=0),
        dcc.Download(id='download-event')
    ]),
    html.Div(id='feedback', style={'marginTop': '20px'}),
    #html.Hr(),
    html.Div(id='event-list-container', style={'marginTop': '20px'})
])


# Callback to populate event options and fill inputs for editing
@app.callback(
    [Output('event-select', 'options'),
     Output('edit-title', 'value'),
     Output('edit-date', 'value'),
     Output('edit-location', 'value'),
     Output('edit-description', 'value')],
    Input('event-select', 'value'),
    Input('save-event-btn', 'n_clicks'),
    Input('add-new-event-btn', 'n_clicks')
)
def populate_edit_form(selected_event_id,n_clicks,n_clicks2):
    events = Event.objects.all()
    dropdown_options = [{'label': f"{event.title} - {event.date}", 'value': event.id} for event in events]
    if selected_event_id:
        event = Event.objects.get(id=selected_event_id)
        return dropdown_options, event.title, event.date, event.location, event.description
    return dropdown_options, "", "", "", ""


# Callback to handle adding or editing an event
@app.callback(
    Output('feedback', 'children'),
    [Input('save-event-btn', 'n_clicks'),
     Input('add-new-event-btn', 'n_clicks')],
    [State('event-select', 'value'),
     State('edit-title', 'value'),
     State('edit-date', 'value'),
     State('edit-location', 'value'),
     State('edit-description', 'value')]
)
def save_or_add_event(save_clicks, add_clicks, event_id, title, date, location, description):
    triggered_id = ctx.triggered_id
    if triggered_id == 'save-event-btn' and save_clicks > 0:
        if event_id:
            event = Event.objects.get(id=event_id)
            event.title = title
            event.date = date
            event.location = location
            event.description = description
            event.save()
            return f"Event '{event.title}' has been updated."
        return "Error: No event selected to edit."

    if triggered_id == 'add-new-event-btn' and add_clicks > 0:
        if title and date and location:
            Event.objects.create(title=title, date=date, location=location, description=description)
            return f"Event '{title}' has been added."
        return "Error: Please fill in all required fields (Title, Date, Location)."

    return ""


# Callback to handle the file download
@app.callback(
    Output('download-event', 'data'),
    Input('download-btn', 'n_clicks'),
    State('event-select', 'value')
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
            worksheet.insert_image('A1', 'sine_wave.png', {'image_data': plot_buffer})

        buffer.seek(0)

        # Use Dash's native dcc.Download
        return dcc.send_bytes(buffer.getvalue(), filename=f"Event_{event.title}.xlsx")
    return None


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
