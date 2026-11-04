import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest

import main


@pytest.fixture
def game(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "HIGHSCORE_FILE", str(tmp_path / "highscore.txt"))
    return main.GameManager()


def add_word(game, text="Да"):
    word = main.Word(text, 100, 100, game.wave)
    game.words.append(word)
    return word


def test_wave_word_count():
    assert main.get_wave_word_count(1) == 10
    assert main.get_wave_word_count(3) == 20


def test_typing_is_case_insensitive():
    word = main.Word("Кот", 0, 0, 1)

    assert word.type_char("к")
    assert not word.type_char("x")
    assert word.type_char("О") and word.type_char("т")
    assert word.is_complete()


def test_destroying_a_word_scores(game):
    game.destroy_word(add_word(game, "Мама"))

    assert game.score == 4
    assert game.words == []


def test_wave_advances_after_enough_words(game):
    for _ in range(main.get_wave_word_count(1)):
        game.destroy_word(add_word(game))

    assert game.wave == 2
    assert game.wave_destroyed == 0
    assert game.wave_message is not None


def test_word_reaching_the_planet_damages_the_ship(game):
    word = add_word(game)
    word.y = main.SCREEN_HEIGHT

    game.update()

    assert game.player.health == 100 - main.WORD_DAMAGE
    assert word not in game.words


def test_game_over_saves_highscore_and_reset_restarts(game):
    game.score = 42
    game.player.health = main.WORD_DAMAGE
    add_word(game).y = main.SCREEN_HEIGHT

    game.update()

    assert game.state == main.GameState.GAME_OVER
    assert main.load_highscore() == 42

    game.reset()

    assert game.state == main.GameState.PLAYING
    assert game.score == 0
    assert game.player.health == 100
    assert game.highscore == 42


def test_highscore_ignores_bad_file(tmp_path):
    path = tmp_path / "highscore.txt"
    path.write_text("abc", encoding="utf-8")

    assert main.load_highscore(str(path)) == 0
    assert main.load_highscore(str(tmp_path / "missing.txt")) == 0


def test_draw_does_not_fail(game):
    game.game_over()
    game.draw()
