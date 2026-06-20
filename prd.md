Requirements Document
1. Application Overview
Application Name: Flood Watch

Description: A web-based flood risk monitoring dashboard designed for city planners and disaster response agencies to track flood risk across Nairobi and Dar es Salaam using satellite-derived water index data, rainfall trends, and historical flood records. The application provides real-time risk assessment, early warning alerts, and mitigation insights to support operational decision-making.

2. Users and Usage Scenarios
Target Users:

City mayors and municipal officials
County/municipal disaster response teams
Urban planners and infrastructure managers
Emergency operations center staff
Core Usage Scenarios:

Monitor real-time flood risk levels across city neighborhoods
Identify high-risk zones requiring immediate attention
Analyze historical flood patterns and seasonal trends
Receive early warning alerts for potential flood events
Review mitigation strategies and infrastructure measures
Compare flood risk between two cities for resource allocation
3. Page Structure and Functional Description
3.1 Page Hierarchy
Flood Watch Dashboard
├── Overview (landing page)
├── Risk Map
├── Trends
├── Alerts
├── Mitigation & Management Insights
└── Data Sources / Methodology
3.2 Persistent UI Components
3.2.1 Left Sidebar
Display application logo "Flood Watch"
Navigation menu items: Overview, Risk Map, Trends, Alerts, Mitigation Insights, Data Sources
Highlight active page in navigation
3.2.2 Top Bar
City switcher control (segmented control or dropdown) with options: "Nairobi" / "Dar es Salaam"
"Last updated" timestamp
Current city-wide risk level badge
Date range selector
3.3 Overview Page
3.3.1 KPI Cards Row
Display 4-5 key performance indicators for the selected city:

City-wide Flood Risk Index (0-100 gauge visualization)
Number of Active Alert Zones
Population in High-Risk Areas (estimated count)
7-Day Rainfall Forecast (millimeters)
Rivers/River Segments Above Warning Level (count)
3.3.2 Two-Column Layout
Left Column - Compact Risk Map:

Display interactive map centered on selected city
Show flood risk overlay across river corridors and neighborhoods
Enable basic zoom and pan interactions
Right Column - High-Risk Neighborhoods List:

Display top 8 highest-risk neighborhoods ranked by current risk score
For each neighborhood show:
Neighborhood name
Risk level pill (Low/Moderate/High/Severe) with color coding
14-day risk trend sparkline
Estimated households at risk
3.3.3 Alert Banner
Display prominent red banner when any zone reaches Severe risk level
Include "View Details" link to Alerts page
3.3.4 Compare Cities Toggle
Enable side-by-side comparison view
Display both cities' city-wide risk index
Show top-3 highest-risk neighborhoods for each city
3.4 Risk Map Page
3.4.1 Interactive Map Display
Center map on selected city coordinates:
Nairobi: -1.2921, 36.8219
Dar es Salaam: -6.7924, 39.2083
Render flood risk as heatmap/choropleth overlay color-graded from green (low) through yellow/orange (moderate/high) to deep red (severe)
Display NDWI-derived water extent layer showing surface water presence and saturated ground
Overlay river system as blue vector lines for selected city
3.4.2 Map Legend
Explain color intensity reflects Normalized Difference Water Index (NDWI) values
Show risk level color scale (green to red)
Indicate NDWI threshold values (0.2+ elevated, 0.4+ severe)
3.4.3 Layer Toggle Control
Provide toggles for:

NDWI Flood Extent
Risk Zones
River Corridors
Population Density
Drainage Infrastructure
3.4.4 Neighborhood Detail Panel
When user clicks any neighborhood polygon, display side panel with:

Current risk score
NDWI trend sparkline (last 30 days)
Rainfall data (last 7 days and last 30 days)
River gauge level (if applicable)
Population estimate
Number of past flood incidents recorded
3.4.5 Time Slider
Position beneath map
Allow scrubbing through last 12 months
Animate flood-extent overlay changes as user moves slider
Update all map layers to reflect selected time period
3.5 Trends Page
3.5.1 Rainfall vs. Flood Incidents Chart
Multi-line chart showing monthly rainfall (mm) and historical flood incident count from 2018-2026
Annotate city-specific flood events:
Nairobi: 2024 long-rains floods, March 2026 flood event
Dar es Salaam: April 2023, January 2024, December 2019 events
3.5.2 NDWI Index Trend Chart
Area chart displaying city-wide NDWI index over last 24 months
Include shaded threshold band indicating "flood risk" zone
3.5.3 Flood Incidents by Neighborhood Chart
Bar chart showing incidents per neighborhood
Provide toggle between "incident count" and "estimated households affected"
Enable sorting by value
3.5.4 Neighborhood Risk Comparison Grid
Display 6 mini line charts in small multiples layout
Show risk trend for city's six highest-profile flood-prone neighborhoods
3.5.5 Seasonal Calendar Heatmap
Display daily rainfall intensity across the year in calendar grid format
Visualize long-rains/short-rains seasonal patterns:
Nairobi: March-May (long rains), October-December (short rains)
Dar es Salaam: March-May (Masika long rains), October-December (Vuli short rains)
3.6 Alerts Page
3.6.1 Alert Feed
Display operational alert list for selected city, each alert showing:

Neighborhood name
Risk level badge (Low/Moderate/High/Severe)
Trigger reason (e.g., "NDWI threshold exceeded", "River gauge above warning level", "72-hr rainfall forecast >50mm")
Time issued
Recommended action (e.g., "Notify Mathare sub-county office", "Pre-position rescue boats — Jangwani")
3.6.2 Risk Legend
Display 4-tier risk classification with color coding:
Low (green)
Moderate (yellow)
High (orange)
Severe (red)
Include plain-language operational descriptions for each tier
3.6.3 Alert Subscription Panel
Display "Subscribe to alerts" interface
Show SMS/email toggle options (non-functional UI)
3.7 Mitigation & Management Insights Page
Organize insights as cards or accordion sections:

3.7.1 Infrastructure Measures
Nairobi: Nairobi Rivers Regeneration Programme (riparian corridor restoration across 37 mapped areas)
Dar es Salaam: Msimbazi Basin Development Project (World Bank/Spain/Netherlands funded, ~$260M, 2022-2028) covering river dredging, terracing, and floodplain conversion to green park with resettlement/compensation
Include short rationale and potential impact indicator (estimated reduction in exposed population)
3.7.2 Early Warning & Community Measures
Community-based flood spotters
SMS alert networks
Evacuation route mapping for high-density flood-prone settlements
Include rationale and impact indicators
3.7.3 Policy & Land-Use Measures
Enforcement of riparian/riverine setback zones
Relocation/resettlement planning
Building code enforcement in flood corridors
Include rationale and impact indicators
3.7.4 Long-Term Resilience
Green infrastructure initiatives
River corridor restoration
Climate-adaptive urban planning
Include rationale and impact indicators
3.8 Data Sources / Methodology Page
3.8.1 Data Sources by City
Nairobi:

Sentinel-2 / Landsat satellite imagery for NDWI calculation
Kenya Meteorological Department rainfall data
Nairobi Rivers Regeneration Programme mapping
Dar es Salaam:

Sentinel-2 / Landsat satellite imagery for NDWI calculation
Tanzania Meteorological Authority rainfall data
World Bank Msimbazi Basin Development Project data
3.8.2 Methodology Description
Explain NDWI calculation approach (shared methodology for both cities)
Describe risk scoring algorithm
3.8.3 Disclaimer
Display clear statement that data is illustrative/simulated for demonstration purposes
4. Business Rules and Logic
4.1 City Switching Logic
When user selects a city from top bar switcher, update all data-driven views:
KPI values
Map center coordinates and risk overlay
Neighborhood lists
River corridor displays
Trend charts
Alert feeds
Persist selected city in application state across page navigation
Maintain same UI layout and components for both cities
4.2 City Data Structure
Nairobi Configuration:

Map center: -1.2921, 36.8219
River corridors: Nairobi River, Mathare River, Ngong River
37 flood-prone neighborhoods grouped by corridor:
North corridor (Mathare River): Mathare, Korogocho, Lucky Summer, Kiambiu
Central corridor (Nairobi River): CBD, Globe, Gikomba, Eastleigh, Industrial Area
South corridor (Ngong River): Kibera, Kilimani, South B, South C, Mukuru Kwa Reuben, Mukuru Kwa Njenga
East (downstream): Dandora, Kariobangi, Kayole, Komarock, Njiru, Ruai, Mwiki, Donholm, Savannah, Tassia, Fedha
West (upstream/midstream): Madaraka, Lang'ata, Kawangware, Kangemi, Lavington, Westlands, Parklands, Kileleshwa, Chiromo
Historical flood events: 2024 long-rains floods, March 2026 flood event
Mitigation case study: Nairobi Rivers Regeneration Programme
Dar es Salaam Configuration:

Map center: -6.7924, 39.2083
River corridors: Msimbazi River (35km long, ~271 km² catchment) and tributaries (Sinza, Ubungo/Lubungo, Luhanga, Kinyerezi, Zimbiri, Tandale, Makurumla), Ng'ombe River
Flood-prone neighborhoods grouped by corridor:
Upper Msimbazi corridor: Kinyerezi, Segerea, Ukonga, Gongolamboto, Tabata, Vingunguti
Mid Msimbazi corridor: Buguruni, Kigogo, Tandale, Mchikichini, Mzimuni, Magomeni, Hananasif
Lower Msimbazi / CBD corridor: Jangwani, Upanga West, Ilala, Kariakoo
Ng'ombe River corridor: Mabibo Relini
Other zones: Mbagala, Kigamboni Tuangoma, Mburahati, Mtoni Kijichi, Msasani, Kipawa
Historical flood events: April 2023, January 2024, December 2019 (river rose 2+ meters, Jangwani/Mkwajuni/Kigogo bridges impassable)
Mitigation case study: Msimbazi Basin Development Project
4.3 Risk Scoring Logic
Calculate city-wide Flood Risk Index on 0-100 scale
Classify neighborhood risk into 4 tiers: Low, Moderate, High, Severe
Risk score responds to:
NDWI values (range -1 to 1, with 0.2+ flagged as elevated, 0.4+ as severe)
Rainfall data (7-day and 30-day accumulation)
River gauge levels
Historical flood incident frequency
4.4 Alert Generation Logic
Trigger alerts when:
NDWI threshold exceeded (≥0.2 for elevated, ≥0.4 for severe)
River gauge above warning level
72-hour rainfall forecast >50mm
Assign recommended actions based on risk level and neighborhood characteristics
4.5 Data Consistency Rules
Ensure neighborhood flagged as Severe on Risk Map also appears:
At top of Alerts feed
In Overview page high-risk list
With corresponding risk score in all views
Maintain temporal consistency across Overview, Map, Trends, and Alerts for same time period
4.6 Seasonal Pattern Recognition
Both cities share overlapping rainy seasons:
Long rains: March-May (Kenya: long rains, Tanzania: Masika)
Short rains: October-December (Kenya: short rains, Tanzania: Vuli)
Generate mock data with believable seasonal spikes during these periods
5. Exceptions and Edge Cases
Scenario	Handling
No active alerts for selected city	Display "No active alerts" message in Alerts feed
Neighborhood has no historical flood data	Show "No historical data available" in detail panel
Map layer fails to load	Display error message and retry option
Time slider moved to future date	Disable slider beyond current date
City switcher activated during map interaction	Preserve zoom level, update center and data layers
Multiple neighborhoods at Severe risk	Show count in alert banner, list all in Alerts page
Date range selector spans multiple years	Aggregate data appropriately for charts
User clicks neighborhood with no detail data	Display basic information only (name, current risk level)
6. Acceptance Criteria
User opens Flood Watch dashboard and sees Overview page with Nairobi data displayed by default
User clicks city switcher in top bar and selects "Dar es Salaam"
All KPI cards, map view, neighborhood list, and risk indicators update to show Dar es Salaam data
User navigates to Risk Map page and Dar es Salaam remains selected
User clicks a neighborhood polygon on the map and views detailed risk information in side panel
User drags time slider beneath map and watches flood-extent overlay animate through last 12 months
User navigates to Alerts page and sees current alerts for Dar es Salaam with recommended actions
User switches back to Nairobi using city switcher and confirms all views update to Nairobi data
7. Out of Scope for This Release
Real-time satellite data integration
Automated alert notification delivery via SMS/email
User authentication and role-based access control
Multi-language support beyond English
Historical data export functionality
Integration with external emergency response systems
Predictive flood modeling beyond 7-day forecast
Mobile native applications
Offline mode or data caching
Custom alert threshold configuration by users
Additional cities beyond Nairobi and Dar es Salaam
Real-time collaboration features between agencies
Detailed infrastructure asset management
Budget tracking for mitigation projects
