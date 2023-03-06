def histo_evenement_heure(df):
    df['hour_of_event'] = pd.to_datetime(df['datetime']).dt.hour

    eventdata = pd.DataFrame({'hour_of_event': df['hour_of_event']})
    eventdata['Horaire'] = eventdata['hour_of_event'].apply(lambda x: 'Horaires ouvrés' if 7 <= x <= 18 else 'Horaires non ouvrés')

    fig = px.histogram(eventdata, x='hour_of_event', color='Horaire', nbins=24,
                   labels={'hour_of_event': 'Heure', 'count': 'Somme'},
                   category_orders={'Horaire': ['Horaires ouvrés', 'Horaires non ouvrés']},
                   color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(title='Evenements par heure', yaxis_title='Somme', xaxis_title='',
                  xaxis=dict(dtick=1, tick0=0, range=[0, 24]), bargap=0.1)
    fig.update_traces(hovertemplate='Horaire: %{legendgroup}<br>Heure: %{x}<br>Count: %{y}')
    fig.show()
    
histo_evenement_heure(df)