# Contributing to Linnstrument Scale Tool

Thank you for considering contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Linnstrument model)
- Any error messages or logs

### Suggesting Features

We'd love to hear your ideas! Open an issue with:
- A clear description of the feature
- Why it would be useful
- Any examples or mockups if applicable

### Adding Scales

To add a new scale:

1. Edit `scales.py`
2. Add your scale to the `SCALES` dictionary:
   ```python
   SCALES['your_scale_name'] = [0, 2, 3, 5, 7, 8, 10]  # intervals in semitones
   ```
3. Test it: `./run.sh C your_scale_name`
4. Submit a pull request with a description

### Code Contributions

1. **Fork the repository**

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments where helpful
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Test the command-line tool
   ./run.sh C major

   # Run examples
   source venv/bin/activate
   python examples.py
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Description of your changes"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

```bash
# Clone the repo
git clone https://github.com/CommmandrCody/LinnstrumentScaleTool.git
cd LinnstrumentScaleTool

# Install dependencies
./install.sh

# Activate virtual environment
source venv/bin/activate

# Make changes and test
python scale_tool.py C major
```

## Code Style

- Use Python 3.7+ compatible code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Keep functions focused and reasonably sized
- Use descriptive variable names

## Documentation

When adding features, please update:
- Docstrings in the code
- README.md (if it's a major feature)
- QUICK_REFERENCE.md (if it's a common use case)
- Add examples to `examples.py` if appropriate

## Testing

Before submitting a PR:
- Test with your Linnstrument connected
- Verify all existing functionality still works
- Test on macOS if possible (Windows/Linux testing appreciated too)
- Check that `./install.sh` works from a fresh clone

## Areas for Contribution

Here are some ideas if you want to help but aren't sure where to start:

### Easy
- Add new scales to `scales.py`
- Improve documentation
- Add more examples to `examples.py`
- Test on Windows/Linux and report issues
- Create tutorials or videos

### Medium
- Improve the Max for Live device UI
- Add more color schemes
- Support for other grid controllers
- Add configuration file support
- Create a simple GUI wrapper

### Advanced
- Real VST3/AU plugin (requires C++/JUCE)
- Ableton Push integration
- Scale detection improvements
- MIDI learn for scale changes
- Multi-Linnstrument support
- Web-based remote control

## Questions?

- Open an issue for questions about contributing
- Check existing issues and PRs to avoid duplicates
- Be respectful and constructive in discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Credits

Contributors will be acknowledged in the README.md file.

Thank you for helping make this tool better! 🎹✨
