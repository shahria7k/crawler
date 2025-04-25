# Company Data Crawler - Beginner's Guide 🚀

This guide explains how the crawler works in simple terms, step by step. No programming experience required!

## How Does It Work? 🤔

Think of this crawler like a smart robot that visits websites to collect information about companies. Here's what
happens when you run it:

### 1. Starting Up 🌟

When you start the program (`python src/main.py`):

- The crawler wakes up
- Connects to a database (MongoDB)
- Gets ready to visit websites
- Loads its configuration (which websites to visit, how fast to go, etc.)

### 2. The Crawling Process 🕷️

#### Step 1: Finding Websites

- Starts with a list of initial websites (like Crunchbase, AngelList)
- Makes a "to-visit" list of these websites

#### Step 2: Visiting Websites

- Takes a website from the "to-visit" list
- Uses a web browser (Playwright) to visit the site
- Just like you visiting a website, but automated!

#### Step 3: Collecting Information

When on a website, it looks for:

- Company name
- Contact details
- What technology they use
- Social media links
- Employee information
- Location

#### Step 4: Storing Information

- Saves all found information in the database
- Makes sure not to save the same information twice

#### Step 5: Finding More Websites

- While on a website, it looks for links to other company websites
- Adds new found websites to its "to-visit" list
- The cycle continues!

### 3. Being a Good Robot 🤖

The crawler is designed to be polite:

- Doesn't visit websites too quickly (waits between visits)
- Uses different internet connections (proxies) to avoid overloading websites
- Only visits allowed websites
- Respects website rules

### 4. Handling Problems 🛠️

If something goes wrong:

- Automatically tries again
- Skips problematic websites
- Keeps a log of what went wrong
- Continues working with other websites

## What's Happening Behind the Scenes? 🎬

Here's a simple flow of what happens:

```
1. Start
   ↓
2. Load settings
   ↓
3. Connect to database
   ↓
4. Start multiple workers
   ↓
5. For each worker:
   │
   ├─→ Get a website to visit
   │   ↓
   ├─→ Visit the website
   │   ↓
   ├─→ Collect information
   │   ↓
   ├─→ Save information
   │   ↓
   └─→ Find new websites to visit
       (then back to "Get a website")
```

## The Parts Working Together 🔄

Think of it like a factory:

- **Orchestrator**: The factory manager (coordinates everything)
- **Discovery Service**: The map reader (finds new websites to visit)
- **Crawler Service**: The explorer (visits websites)
- **Parser Service**: The researcher (collects information)
- **Storage Service**: The librarian (saves information)

## What You Get 📊

After running the crawler, you'll have:

- A database full of company information
- Logs showing what the crawler did
- Information organized and ready to use

## Common Questions ❓

**Q: How long does it take to crawl websites?** A: It depends on how many websites you're crawling and your settings.
The crawler can visit multiple websites at once!

**Q: What if a website is down?** A: The crawler will skip it and try again later.

**Q: Can it crawl any website?** A: It's designed to crawl business/company websites, but you need to make sure you have
permission to crawl them.

**Q: How do I know it's working?** A: You can watch the logs (crawler.log) to see what it's doing in real-time.

## Need Help? 🆘

If something's not working:

1. Check the logs
2. Make sure MongoDB is running
3. Verify your internet connection
4. Check if the websites you're trying to crawl are accessible

Remember: The crawler is like a helpful robot - it needs clear instructions and the right conditions to work well! 🤖✨
