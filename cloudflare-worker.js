// Cloudflare Worker - Notion API Proxy with Transformation & Caching
// This is the SINGLE SOURCE OF TRUTH for Notion → Gantt data transformation
// 
// Setup Required:
// 1. Deploy to Cloudflare Workers
// 2. Add KV Namespace binding: GANTT_CACHE
// 3. Add Environment Variable: NOTION_API_KEY
// 4. Optional: Add Cron Trigger for scheduled updates

const DATABASE_ID = '291cdd12fc5e81ceafeadc78e6c03258';
const CACHE_KEY = 'gantt_data';
const CACHE_TTL = 3600; // 1 hour cache

export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': 'https://www.mlcl.ai',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Only allow GET
    if (request.method !== 'GET') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const url = new URL(request.url);
      const forceRefresh = url.searchParams.get('refresh') === 'true';
      
      // Try cache first (unless force refresh)
      if (!forceRefresh && env.GANTT_CACHE) {
        const cached = await env.GANTT_CACHE.get(CACHE_KEY);
        if (cached) {
          return new Response(cached, {
            headers: { 
              'Content-Type': 'application/json',
              'X-Cache': 'HIT',
              ...corsHeaders 
            }
          });
        }
      }

      // Fetch fresh data from Notion
      console.log('Fetching from Notion API...');
      const notionPages = await fetchAllNotionPages(DATABASE_ID, env.NOTION_API_KEY);
      
      // Transform to Gantt format (SINGLE SOURCE OF TRUTH)
      const ganttData = transformToGanttFormat(notionPages, DATABASE_ID);
      const jsonData = JSON.stringify(ganttData);
      
      // Cache it in Cloudflare KV
      if (env.GANTT_CACHE) {
        await env.GANTT_CACHE.put(CACHE_KEY, jsonData, {
          expirationTtl: CACHE_TTL
        });
      }
      
      return new Response(jsonData, {
        headers: { 
          'Content-Type': 'application/json',
          'X-Cache': 'MISS',
          ...corsHeaders 
        }
      });
      
    } catch (error) {
      console.error('Worker error:', error);
      return new Response(JSON.stringify({ 
        error: error.message,
        stack: error.stack 
      }), {
        status: 500,
        headers: { 
          'Content-Type': 'application/json',
          ...corsHeaders 
        }
      });
    }
  },
  
  // Optional: Handle scheduled updates (add Cron Trigger in Cloudflare)
  async scheduled(event, env, ctx) {
    console.log('Running scheduled update...');
    try {
      const notionPages = await fetchAllNotionPages(DATABASE_ID, env.NOTION_API_KEY);
      const ganttData = transformToGanttFormat(notionPages, DATABASE_ID);
      
      if (env.GANTT_CACHE) {
        await env.GANTT_CACHE.put(CACHE_KEY, JSON.stringify(ganttData), {
          expirationTtl: CACHE_TTL
        });
      }
      console.log(`Updated cache with ${ganttData.task_count} tasks`);
    } catch (error) {
      console.error('Scheduled update failed:', error);
    }
  }
};

/**
 * Fetch all pages from Notion database with pagination
 */
async function fetchAllNotionPages(databaseId, apiKey) {
  let allResults = [];
  let hasMore = true;
  let startCursor = null;
  
  while (hasMore) {
    const response = await fetch(
      `https://api.notion.com/v1/databases/${databaseId}/query`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Notion-Version': '2022-06-28',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(startCursor ? { start_cursor: startCursor } : {})
      }
    );
    
    if (!response.ok) {
      throw new Error(`Notion API error: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    allResults = allResults.concat(data.results);
    hasMore = data.has_more || false;
    startCursor = data.next_cursor;
  }
  
  return allResults;
}

/**
 * Transform Notion pages to Gantt chart format
 * This is the SINGLE SOURCE OF TRUTH for data transformation
 */
function transformToGanttFormat(notionPages, databaseId) {
  // Extract category color mappings from the first page's schema
  const categoryColors = {};
  if (notionPages.length > 0) {
    const categoryProp = notionPages[0].properties.Category;
    if (categoryProp?.select) {
      // Get color from the actual select value
      const selectValue = categoryProp.select;
      if (selectValue) {
        categoryColors[selectValue.name] = notionColorToHex(selectValue.color);
      }
    }
  }
  
  const tasks = notionPages.map(page => {
    const props = page.properties;
    
    const owner = extractPeople(props.Owner);
    const contributors = extractPeople(props.Contributors);
    const category = extractSelect(props.Category);
    
    // Get color from the select option
    let categoryColor = null;
    if (props.Category?.select) {
      categoryColor = notionColorToHex(props.Category.select.color);
    }
    
    return {
      id: page.id,
      name: extractText(props['Task/Project Name']),
      category: category,
      category_color: categoryColor,
      start_date: extractDate(props['Start Date']),
      end_date: extractDate(props['End Date']),
      status: extractStatus(props.Status),
      priority: extractSelect(props.Priority),
      owner: owner && owner.length > 0 ? owner[0] : null,
      contributors: contributors || [],
      progress: props.Progress?.number || null,
      tags: extractMultiSelect(props.Tags),
      one_time_cost: props['One-Time Cost']?.number || null,
      monthly_cost: props['Monthly Cost']?.number || null,
      blocked_by: extractRelation(props['Blocked by']),
      blocking: extractRelation(props.Blocking),
    };
  });
  
  return {
    exported_at: new Date().toISOString(),
    database_id: databaseId,
    task_count: tasks.length,
    tasks: tasks
  };
}

// Property extraction helpers
function extractText(prop) {
  if (!prop) return null;
  if (prop.type === 'title') return prop.title.map(t => t.plain_text).join('');
  if (prop.type === 'rich_text') return prop.rich_text.map(t => t.plain_text).join('');
  return null;
}

function extractSelect(prop) {
  return prop?.select?.name || null;
}

function extractMultiSelect(prop) {
  return prop?.multi_select?.map(s => s.name) || [];
}

function extractStatus(prop) {
  return prop?.status?.name || null;
}

function extractDate(prop) {
  return prop?.date?.start || null;
}

function extractPeople(prop) {
  if (!prop?.people) return [];
  return prop.people.map(p => p.name || p.id);
}

function extractRelation(prop) {
  return prop?.relation?.map(r => r.id) || [];
}

// Convert Notion color names to hex codes
function notionColorToHex(notionColor) {
  const colorMap = {
    'default': '#95a5a6',
    'gray': '#95a5a6',
    'brown': '#8B4513',
    'orange': '#e67e22',
    'yellow': '#f39c12',
    'green': '#2ecc71',
    'blue': '#3498db',
    'purple': '#9b59b6',
    'pink': '#e91e63',
    'red': '#e74c3c'
  };
  return colorMap[notionColor] || '#95a5a6';
}
