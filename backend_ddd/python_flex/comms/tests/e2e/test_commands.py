from python_flex.comms.entrypoint import commands


def test_send_email():
    commands.send_email(
        subject="Pytest",
        text="Woah noice content, someone ran pytest and the email got into your inbox successfully!",
        to="23100011@lums.edu.pk",
    )
