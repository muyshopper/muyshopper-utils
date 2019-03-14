"""PushBullet notifications utilities."""
import argparse
import datetime
from pushbullet import Pushbullet


class NotificationManager:
    """Manage pushbullet notifications."""

    def __init__(self):
        """Notification manager constructor."""
        ACCESS_TOKEN = 'o.Q7JCeZInrTVCG4RwdDrqD4kuJuX5cggd'
        CHANNEL_TAG = 'muyshopper'

        pb = Pushbullet(ACCESS_TOKEN)
        self.ms_channel = pb.get_channel(CHANNEL_TAG)

    def push_notification(self, title, message):
        """Push notification to the MuyShopper pushbullet channel."""
        push = self.ms_channel.push_note(title, message)
        return push


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--message', '-m', required=True)
    args = parser.parse_args()

    message = args.message

    notification_manager = NotificationManager()

    date = datetime.date.strftime(datetime.datetime.now(), '%d/%m/%y')

    notification_manager.push_notification(
        title='Notificacion MuyShopper ({})'.format(date),
        message=message,
    )
