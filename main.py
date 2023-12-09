from website import create_app
import os
from datetime import timedelta, datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()


def cleanup_expired_sessions():
    session_folder = 'flask_session'

    # Lista dei file nella cartella delle sessioni
    session_files = os.listdir(session_folder)

    # Timestamp attuale
    current_timestamp = datetime.now().timestamp()

    for session_file in session_files:
        file_path = os.path.join(session_folder, session_file)

        # Ottieni l'ultima modifica del file (timestamp)
        last_modified_timestamp = os.path.getmtime(file_path)

        # Calcola l'età della sessione in secondi
        session_age = current_timestamp - last_modified_timestamp

        # Durata massima della sessione
        max_session_age = 365 * 24 * 60 * 60

        # Se la sessione è scaduta, elimina il file
        if session_age > max_session_age:
            os.remove(file_path)


if __name__ == '__main__':

    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_expired_sessions, 'interval', hours=1)
    scheduler.start()

    app.run(port=5000, debug=True)

