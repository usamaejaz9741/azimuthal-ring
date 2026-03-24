import pytest
from unittest.mock import patch, MagicMock
import bot

def test_main():
    # Mocking all external calls to avoid starting a real bot
    with patch('database.init_db') as mock_db:
        # Mocking ApplicationBuilder
        # Using a SPECIFIC path for ApplicationBuilder if it's imported in bot.py
        with patch('bot.ApplicationBuilder') as mock_app_builder:
            mock_app = MagicMock()

            mock_builder_instance = MagicMock()
            mock_app_builder.return_value = mock_builder_instance
            mock_builder_instance.token.return_value = mock_builder_instance
            mock_builder_instance.build.return_value = mock_app

            with patch('scheduler.init_scheduler') as mock_init_scheduler:
                with patch('bot.TELEGRAM_TOKEN', '123:abc'):
                    with patch('builtins.print'):
                        # To be safe, also mock run_polling on mock_app
                        mock_app.run_polling = MagicMock()

                        bot.main()

                        mock_db.assert_called_once()
                        mock_builder_instance.token.assert_called_with('123:abc')
                        mock_init_scheduler.assert_called_once_with(mock_app.bot)
                        mock_app.run_polling.assert_called_once()
