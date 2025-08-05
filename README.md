# Xiaohongshu AI Automation System

An advanced AI-powered automation solution for Xiaohongshu (Little Red Book) content creation and management. This intelligent system combines psychological growth tracking, automated content generation, and strategic posting to maintain an engaging social media presence.

## 🌟 Features

### 🤖 Intelligent Content Generation
- **AI-Driven Content Creation**: Leverages advanced language models (Qwen) to generate authentic, engaging posts
- **Personality-Based Writing**: Maintains consistent voice and character development across all content
- **Dynamic Title Generation**: Creates compelling titles based on content and psychological state
- **Multi-source News Analysis**: Aggregates and analyzes trending topics from major platforms

### 📊 Psychological Growth Management
- **Big Five Personality Tracking**: Monitors and evolves personality traits over time
- **Emotional Intelligence Development**: Tracks self-awareness, social awareness, and relationship management
- **Growth Milestone Recording**: Documents psychological development journey
- **Adaptive Content Strategy**: Adjusts content tone based on psychological profile

### 🔄 Automated Workflow
- **Scheduled News Collection**: Daily automated gathering from 5+ major news sources
- **Content Analysis Pipeline**: AI-powered analysis of trending topics and cultural insights
- **Automated Publishing**: Seamless posting to Xiaohongshu with images and optimized timing
- **Performance Tracking**: Comprehensive logging of posts, engagement, and growth metrics

### 🛠️ Technical Integration
- **MCP Server Architecture**: Modern client-server design for reliable automation
- **Jina Reader API Integration**: Advanced web content extraction and analysis
- **Flexible Scheduling**: Customizable posting schedules with cron-like functionality
- **Comprehensive Logging**: Detailed activity logs for monitoring and optimization

## 📋 Requirements

- Python 3.8+
- Xiaohongshu account
- API Keys:
  - Qwen API key (for content generation)
  - Jina API key (for web content extraction)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/chengyixu/xhs-ai-automation.git
   cd xhs-ai-automation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

4. **Run the automation**
   ```bash
   # Manual mode
   python xhs_ai_powered_client.py --manual
   
   # Daemon mode (scheduled automation)
   python xhs_ai_powered_client.py --daemon
   
   # Single run
   python xhs_ai_powered_client.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Xiaohongshu Configuration
XHS_PHONE=your_phone_number
XHS_JSON_PATH=./cookies
XHS_IMAGE_PATH=./images/default.png

# AI API Configuration
QWEN_API_KEY=your_qwen_api_key
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-plus

# Jina API Configuration
JINA_API_KEY=your_jina_api_key

# File Storage
XHS_BASE_PATH=./data
```

### Directory Structure

```
xhs-ai-automation/
├── data/                    # Data storage directory
│   ├── personality.json     # Personality profile
│   ├── understandings.json  # World understanding data
│   ├── memories.json        # Analysis memories
│   ├── posts.json          # Post history
│   └── knowledge.json      # Knowledge base
├── cookies/                # Authentication cookies
├── images/                 # Images for posts
├── logs/                   # Application logs
├── xhs_ai_powered_client.py    # Main application
├── psychological_growth_manager.py  # Psychological growth module
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 📊 Usage Modes

### Manual Mode
Interactive command-line interface for manual control:
- Collect and analyze news on demand
- Generate and publish content manually
- View personality status and statistics
- Test connections and configurations

### Daemon Mode
Automated scheduling for hands-free operation:
- Daily news collection at 17:00
- Content publishing at 18:00
- Continuous psychological growth tracking
- Automatic error recovery

### Single Run Mode
Execute one complete cycle:
- Collect news → Analyze → Generate content → Publish
- Useful for testing and one-off operations

## 🧠 Psychological Growth System

The system includes a sophisticated psychological growth manager that:

- Tracks personality evolution using the Big Five model
- Develops emotional intelligence over time
- Records growth milestones and achievements
- Influences content generation based on psychological state

This creates more authentic and evolving content that reflects a developing personality.

## 📈 Performance Metrics

The system tracks:
- Total posts published
- News sources analyzed
- Psychological growth milestones
- Content engagement patterns
- System uptime and reliability

## 🔒 Security Considerations

- API keys are stored in environment variables
- Cookies are kept in a secure directory
- Logs contain no sensitive information
- All data is stored locally

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Qwen for advanced language modeling
- Jina AI for web content extraction
- Xiaohongshu MCP server for platform integration

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

**Note**: This tool is for educational and personal use. Please ensure compliance with Xiaohongshu's terms of service and respect platform guidelines.