# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2025-03-10

### Added
- ✨ ZIP file upload and processing feature
  - Upload ZIP archives containing multiple documents
  - Automatic extraction and processing of each file within the archive
  - Support for nested folders in ZIP files
  - Added ZIP file format to supported formats list in UI

## [1.0.0] - 2025-03-10

### Added
- ✨ Animated document upload progress indicator
  - Visual feedback during document processing
  - Multi-step animation showing upload progress stages
  - Improved user experience for longer uploads

### Fixed
- 🚑 Corrected refresh functionality in admin panel
  - Fixed "Refresh Models" button to trigger correct API endpoint
  - Improved loading state display and error handling
  - Better user experience during model refresh

### Added
- ✨ Singleton pattern to ModelService
  - Improved model initialization process
  - Added refresh_models method to explicitly refresh available models
  - Force refresh option for models

### Changed
- ♻️ Improved model updating logic
  - Added fetching models from Anthropic API for Claude models
  - Process API response and update models list
  - Set first fetched model as default when needed
- ♻️ Updated services to use ModelService configuration
  - OpenAIService, OllamaService, ClaudeService now use ModelService
  - Services load model configuration from JSON instead of environment variables
  - Implemented fallback mechanisms to default models

### Fixed
- 🚑 Updated package versions in requirements.txt
- 🚑 Added additional platforms to Docker build job
- 🚑 Removed version field from docker-compose files
- 🚑 Updated Qdrant host in .env.example

## [0.9] - 2025-03-09

- Initial commit with basic functionality