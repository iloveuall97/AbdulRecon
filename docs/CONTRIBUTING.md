# 🤝 Contributing - AegisRecon Pro

## Code of Conduct

All contributors must:
- Use this tool for authorized testing only
- Respect ethical hacking principles
- Never use for unauthorized access
- Follow security best practices

## How to Contribute

### 1. Fork Repository
```bash
git clone https://github.com/yourusername/AbdulRecon.git
cd AbdulRecon
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Write clean, well-documented code
- Follow existing code style
- Add tests for new features
- Update documentation

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## Development Setup

```bash
# Install development dependencies
cd backend
pip install -r requirements.txt
pip install black flake8 pylint

cd ../frontend
npm install
npm install --save-dev eslint prettier
```

## Code Style

### Python
- Use Black for formatting
- Follow PEP 8
- Use type hints
- Write docstrings

```python
def detect(self, url: str, parameters: Dict[str, str]) -> List[Dict[str, Any]]:
    """Detect vulnerabilities in target.
    
    Args:
        url: Target URL
        parameters: Parameters to test
    
    Returns:
        List of detected vulnerabilities
    """
    pass
```

### JavaScript/React
- Use Prettier for formatting
- Use ESLint for linting
- Use functional components with hooks
- Write meaningful component names

```javascript
const ScanProgress = ({ progress, status }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {/* Component JSX */}
    </motion.div>
  )
}
```

## Adding New Vulnerability Detectors

### Step 1: Create Module Directory
```bash
mkdir backend/modules/my_detector
touch backend/modules/my_detector/__init__.py
touch backend/modules/my_detector/detector.py
```

### Step 2: Implement Detector
```python
# backend/modules/my_detector/detector.py
from ..base_module import BaseVulnerabilityDetector

class MyDetector(BaseVulnerabilityDetector):
    """My vulnerability detector"""
    
    async def detect(self, url: str, parameters: Dict[str, str]):
        """Implement detection logic"""
        findings = []
        # Your detection code here
        return findings
    
    def get_payloads(self) -> List[str]:
        """Return test payloads"""
        return []
```

### Step 3: Register Module
```python
# backend/modules/my_detector/__init__.py
from .detector import MyDetector

__all__ = ['MyDetector']
```

## Adding Frontend Features

### Step 1: Create Component
```javascript
// frontend/src/components/MyComponent.jsx
import { motion } from 'framer-motion'

const MyComponent = ({ data }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="...."
    >
      {/* JSX here */}
    </motion.div>
  )
}

export default MyComponent
```

### Step 2: Add to Page
```javascript
// frontend/src/pages/Dashboard.jsx
import MyComponent from '../components/MyComponent'

const Dashboard = () => {
  return (
    <div>
      <MyComponent data={data} />
    </div>
  )
}
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Documentation

When adding features:
1. Update relevant documentation files
2. Add comments to code
3. Update API documentation if applicable
4. Update CHANGELOG.md

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Fill out PR template
4. Link related issues
5. Request review from maintainers
6. Address review feedback
7. Merge when approved

## Reporting Issues

### Security Issues
- Do NOT open public issues
- Email: security@aegisrecon.dev
- Include: Description, Steps, Impact, Suggested Fix

### Bug Reports
1. Use issue template
2. Include:
   - OS and version
   - Python/Node version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Feature Requests
1. Check existing issues first
2. Describe use case
3. Provide examples
4. Explain benefits

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Test additions
- `chore`: Build/config changes

## License

By contributing, you agree that your contributions will be licensed under the project's license.
