(function () {
  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (char) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char];
    });
  }

var SHOTS = {
    empowerid: {
      title: "Access",
      features: ["Role administration", "Access reviews", "Audit-ready history"],
      nav: ["Overview", "Roles", "Reviews", "Audit"],
      kpis: [["Open", "18"], ["In review", "6"], ["Ready", "12"]],
      bars: [42, 68, 50, 86, 60, 74],
      rows: [["Review", "Finance approver", "Today"], ["Role", "Vendor admin", "Queued"], ["Audit", "Weekly export", "Ready"]]
    },
    "profile-management": {
      title: "Profiles",
      features: ["Profile records", "Change history", "Role-based editing"],
      nav: ["People", "Profiles", "Changes", "Access"],
      kpis: [["Profiles", "42"], ["Pending", "7"], ["Updated", "15"]],
      bars: [55, 40, 72, 48, 66, 58],
      rows: [["Update", "Contact details", "Review"], ["Change", "Department", "Saved"], ["Access", "HR editor", "Active"]]
    },
    solidarity: {
      title: "Work",
      features: ["Shared work queue", "Named ownership", "Status the team can see"],
      columns: [
        { name: "New", cards: [["Intake form", "Unassigned"], ["Partner note", "Waiting"]] },
        { name: "Active", cards: [["Follow-up", "Assigned"], ["Site visit", "Today"]] },
        { name: "Done", cards: [["Weekly close", "Recorded"]] }
      ]
    },
    "metro-kiosk": {
      title: "Metro",
      features: ["Ticket purchase flow", "Simple kiosk screens", "Staff path for exceptions"],
      tiles: [["Buy ticket", "Single or return"], ["Top up", "Card balance"], ["Routes", "Next departures"], ["Help", "Staff desk"]]
    },
    integrityweb: {
      title: "Cases",
      features: ["Shared case record", "Ownership and status", "Notes in one place"],
      columns: [
        { name: "Intake", cards: [["New report", "Unassigned"]] },
        { name: "Active", cards: [["Assigned case", "Owner set"], ["Note added", "Today"]] },
        { name: "Closed", cards: [["Resolved", "Filed"]] }
      ]
    },
    "ai-knowledge-assistant": {
      title: "Knowledge",
      features: ["Answers from approved sources", "Source beside the answer", "Control of what it can read"],
      messages: [
        ["Staff", "Where is the travel policy for regional trips?", false],
        ["Assistant", "Section 4 of the approved travel policy. Source shown beside the answer.", true]
      ]
    },
    "ai-document-processing": {
      title: "Extract",
      features: ["File intake", "Suggested fields", "A person confirms before save"],
      lines: [48, 88, 70, 92, 56],
      fields: [["Vendor", "Sample supplier"], ["Invoice", "INV-1044"], ["Amount", "Sample"], ["Status", "Needs review"]]
    },
    "saas-billing": {
      title: "Billing",
      features: ["Plans and subscriptions", "Invoice status", "Account state in one view"],
      nav: ["Plans", "Accounts", "Invoices", "Status"],
      kpis: [["Active", "24"], ["Past due", "3"], ["Drafts", "5"]],
      bars: [60, 78, 44, 70, 52, 66],
      rows: [["Invoice", "Growth plan", "Open"], ["Account", "Trial ending", "Watch"], ["Plan", "Annual", "Active"]]
    },
    "crm-pipeline": {
      title: "Pipeline",
      features: ["Stages with owners", "Next action on each lead", "A board that stays current"],
      columns: [
        { name: "New", cards: [["Inbound", "Unassigned"]] },
        { name: "Talk", cards: [["Discovery", "Owner set"]] },
        { name: "Proposal", cards: [["Quote sent", "Waiting"]] },
        { name: "Won", cards: [["Kickoff", "Handed off"]] }
      ]
    },
    "inventory-warehouse": {
      title: "Stock",
      features: ["SKU and location", "Stock movements", "Low-stock visibility"],
      nav: ["Stock", "Locations", "Moves", "Alerts"],
      kpis: [["SKUs", "128"], ["Low", "9"], ["Inbound", "4"]],
      bars: [70, 46, 82, 38, 64, 58],
      rows: [["Move", "Aisle B", "Received"], ["SKU", "Carton 20", "Low"], ["Dock", "Inbound", "Today"]]
    },
    "hr-leave": {
      title: "Leave",
      features: ["Leave requests", "Balances", "Manager approval"],
      columns: [
        { name: "Requested", cards: [["Annual leave", "3 days"], ["Remote day", "Friday"]] },
        { name: "Review", cards: [["Manager", "Pending"]] },
        { name: "Approved", cards: [["Balance", "Updated"]] }
      ]
    },
    "school-management": {
      title: "School",
      features: ["Student records", "Classes", "Attendance"],
      nav: ["Students", "Classes", "Attendance", "Office"],
      kpis: [["Students", "86"], ["Classes", "12"], ["Absent", "4"]],
      bars: [50, 64, 42, 76, 58, 48],
      rows: [["Class", "Year 4", "Today"], ["Record", "Contact", "Saved"], ["Absence", "Office note", "Open"]]
    },
    "appointment-booking": {
      title: "Bookings",
      features: ["Services and availability", "Confirmed bookings", "A calendar staff can trust"],
      tiles: [["Consult", "30 minutes"], ["Follow-up", "15 minutes"], ["Today", "8 booked"], ["Open slots", "Afternoon"]]
    },
    "ecommerce-catalog": {
      title: "Catalog",
      features: ["Categories and search", "Product records", "Admin merchandising"],
      columns: [
        { name: "Draft", cards: [["New product", "Missing photo"]] },
        { name: "Live", cards: [["Featured", "In category"], ["Searchable", "Published"]] },
        { name: "Review", cards: [["Price check", "Merchandising"]] }
      ]
    },
    "referral-affiliate": {
      title: "Referrals",
      features: ["Referral source", "Conversion status", "Reward state"],
      nav: ["Clicks", "Qualified", "Rewards", "Partners"],
      kpis: [["Clicks", "40"], ["Qualified", "6"], ["Due", "2"]],
      bars: [36, 58, 44, 72, 50, 66],
      rows: [["Click", "Partner link", "Logged"], ["Lead", "Qualified", "Review"], ["Reward", "Pending", "Due"]]
    },
    "notifications-dashboard": {
      title: "Signals",
      features: ["Live event list", "Filters", "Read state"],
      rows: [["Info", "Order updated", "New"], ["Warn", "Sync delayed", "Open"], ["Info", "User invited", "Read"], ["Warn", "Payment retry", "Open"]]
    },
    "analytics-dashboard": {
      title: "Insights",
      features: ["Filters a manager can use", "Trends from stored data", "No five-spreadsheet export"],
      nav: ["Overview", "Trends", "Filters", "Export"],
      kpis: [["Orders", "64"], ["Open", "11"], ["On time", "58"]],
      bars: [48, 70, 62, 84, 56, 74],
      rows: [["Range", "This month", "Applied"], ["Team", "Operations", "Selected"], ["Export", "CSV", "Ready"]]
    },
    "legacy-modernization": {
      title: "Modernize",
      features: ["APIs extracted in stages", "New screens beside the old app", "No reckless rewrite"],
      rows: [["GET", "/customers", "Live"], ["GET", "/orders", "Live"], ["POST", "/auth/token", "New"], ["GET", "/legacy/report", "Bridge"]]
    },
    "document-portal": {
      title: "Documents",
      features: ["Folders and permissions", "Sharing with an expiry", "An audit trail"],
      lines: [40, 86, 64, 78, 52],
      fields: [["Folder", "Contracts"], ["Access", "Legal team"], ["Share", "Expires Friday"], ["Audit", "View recorded"]]
    },
    "api-integration-hub": {
      title: "Integrations",
      features: ["Integrations in one list", "Run and review", "Failures a person can see"],
      rows: [["POST", "/sync/orders", "OK"], ["GET", "/crm/contacts", "OK"], ["POST", "/billing/export", "Retry"], ["GET", "/warehouse/stock", "OK"]]
    },
    "multitenant-admin": {
      title: "Tenants",
      features: ["Tenant settings", "Isolated data access", "An operator console"],
      nav: ["Tenants", "Settings", "Access", "Health"],
      kpis: [["Tenants", "11"], ["Setup", "2"], ["Healthy", "9"]],
      bars: [64, 40, 72, 58, 80, 46],
      rows: [["Tenant", "Setup checklist", "Open"], ["Access", "Admin invite", "Sent"], ["Data", "Isolated", "Checked"]]
    },
    "payment-reconciliation": {
      title: "Reconcile",
      features: ["Suggested matches", "Exception queue", "Export for the close"],
      lines: [52, 90, 68, 80, 44],
      fields: [["Batch", "Sample payout"], ["Matched", "18 lines"], ["Exception", "2 lines"], ["Status", "Needs review"]]
    },
    "remote-sprint-workspace": {
      title: "Sprint",
      features: ["Sprint board with owners", "Remote daily status", "Review-ready story detail"],
      columns: [
        { name: "To do", cards: [["Client API", "Remote"], ["File handoff", "Waiting"]] },
        { name: "Doing", cards: [["Auth review", "Paired"], ["Daily note", "Posted"]] },
        { name: "Review", cards: [["Invoice export", "Ready"]] }
      ]
    },
    "client-delivery-portal": {
      title: "Delivery",
      features: ["Milestone timeline", "Written decision log", "Secure file handoff"],
      nav: ["Milestones", "Decisions", "Files", "Messages"],
      kpis: [["Milestones", "5"], ["In review", "2"], ["Files", "8"]],
      bars: [44, 66, 52, 78, 48, 70],
      rows: [["Decision", "Phase 2 scope", "Open"], ["File", "API notes", "Shared"], ["Milestone", "UAT", "This week"]]
    },
    "enterprise-procurement": {
      title: "Procurement",
      features: ["Request and approval", "Vendor records", "Order status a buyer can see"],
      columns: [
        { name: "Request", cards: [["Office supplies", "New"], ["Software seat", "Draft"]] },
        { name: "Approval", cards: [["Manager", "Pending"]] },
        { name: "Ordered", cards: [["Vendor", "Confirmed"]] }
      ]
    },
    "multisite-operations": {
      title: "Sites",
      features: ["Branch overview", "Exception queue", "Role-based site access"],
      nav: ["Branches", "Exceptions", "Staff", "Reports"],
      kpis: [["Sites", "6"], ["Exceptions", "3"], ["Open", "14"]],
      bars: [58, 42, 74, 50, 66, 60],
      rows: [["Branch", "North desk", "Open"], ["Exception", "Staffing gap", "Today"], ["Access", "Regional lead", "Active"]]
    },
    "saas-onboarding": {
      title: "Onboarding",
      features: ["Tenant setup checklist", "Invites and roles", "First integration status"],
      nav: ["Checklist", "Users", "Integrations", "Plan"],
      kpis: [["Steps", "6"], ["Done", "4"], ["Waiting", "1"]],
      bars: [80, 72, 64, 40, 56, 48],
      rows: [["Step", "Company profile", "Done"], ["Invite", "Admin user", "Sent"], ["API", "First connection", "Waiting"]]
    },
    "ai-support-triage": {
      title: "Support",
      features: ["Suggested category", "Draft reply for review", "Nothing sends without approval"],
      messages: [
        ["Customer", "I was charged twice for the same invoice.", false],
        ["Draft reply", "Suggested category: Billing. A person must approve this before it is sent.", true]
      ]
    },
    "ai-requirements-assistant": {
      title: "Brief",
      features: ["Brief turned into goals", "Open questions called out", "An editable story draft"],
      lines: [62, 84, 54, 76, 48],
      fields: [["Goal", "Book a service online"], ["Question", "Who can cancel?"], ["Story", "Staff sees the day"], ["Status", "Draft"]]
    },
    "service-business-suite": {
      title: "Services",
      features: ["Service booking", "Staff calendar", "Invoice from a completed job"],
      nav: ["Bookings", "Calendar", "Jobs", "Invoices"],
      kpis: [["Today", "8"], ["Staff", "4"], ["Unbilled", "3"]],
      bars: [52, 68, 46, 74, 60, 40],
      rows: [["Booking", "Consult, 10:00", "Confirmed"], ["Staff", "Afternoon shift", "Set"], ["Invoice", "Completed job", "Draft"]]
    }
  };

  function chrome(title) {
    return '<div class="shot__bar"><i></i><i></i><i></i><strong>' + escapeHtml(title) + "</strong><em>Sample UI</em></div>";
  }

  function dashboard(scene) {
    var nav = (scene.nav || ["Overview", "Records", "Activity"]).map(function (item, index) {
      return "<span" + (index === 0 ? ' class="is-on"' : "") + ">" + escapeHtml(item) + "</span>";
    }).join("");
    var kpis = (scene.kpis || []).map(function (pair) {
      return "<p><small>" + escapeHtml(pair[0]) + "</small><strong>" + escapeHtml(pair[1]) + "</strong></p>";
    }).join("");
    var bars = (scene.bars || [46, 72, 54, 84, 63]).map(function (height) {
      return '<i style="--h:' + height + '%"></i>';
    }).join("");
    var rows = (scene.rows || []).map(function (row) {
      return "<li><b>" + escapeHtml(row[0]) + "</b><span>" + escapeHtml(row[1]) + "</span><em>" + escapeHtml(row[2]) + "</em></li>";
    }).join("");
    return '<div class="shot__app"><nav>' + nav + '</nav><div class="shot__main"><div class="shot__kpis">' + kpis + '</div><div class="shot__bars">' + bars + "</div><ul>" + rows + "</ul></div></div>";
  }

  function columns(scene, className) {
    return '<div class="' + className + '">' + (scene.columns || []).map(function (col) {
      var cards = (col.cards || []).map(function (card) {
        return "<article><strong>" + escapeHtml(card[0]) + "</strong><span>" + escapeHtml(card[1]) + "</span></article>";
      }).join("");
      return "<section><h4>" + escapeHtml(col.name) + "</h4>" + cards + "</section>";
    }).join("") + "</div>";
  }

  function kiosk(scene) {
    return '<div class="shot__kiosk">' + (scene.tiles || []).map(function (tile, index) {
      return "<button type=\"button\"" + (index === 0 ? " class=\"is-on\"" : "") + "><strong>" + escapeHtml(tile[0]) + "</strong><span>" + escapeHtml(tile[1]) + "</span></button>";
    }).join("") + "</div>";
  }

  function chat(scene) {
    return '<div class="shot__chat">' + (scene.messages || []).map(function (message) {
      return '<p class="who">' + escapeHtml(message[0]) + '</p><p class="bubble' + (message[2] ? " me" : "") + '">' + escapeHtml(message[1]) + "</p>";
    }).join("") + "</div>";
  }

  function doc(scene) {
    var lines = (scene.lines || [70, 92, 60, 84]).map(function (width) {
      return '<i style="--w:' + width + '%"></i>';
    }).join("");
    var fields = (scene.fields || []).map(function (field) {
      return "<div><dt>" + escapeHtml(field[0]) + "</dt><dd>" + escapeHtml(field[1]) + "</dd></div>";
    }).join("");
    return '<div class="shot__doc"><div class="shot__paper">' + lines + '</div><dl class="shot__fields">' + fields + "</dl></div>";
  }

  function endpoints(scene) {
    var rows = (scene.rows || []).map(function (row) {
      return "<li><b>" + escapeHtml(row[0]) + "</b><span>" + escapeHtml(row[1]) + "</span><em>" + escapeHtml(row[2]) + "</em></li>";
    }).join("");
    return '<div class="shot__main shot__main--full"><ul>' + rows + "</ul></div>";
  }

  var layouts = {
    dashboard: dashboard,
    board: function (scene) { return columns(scene, "shot__board"); },
    pipeline: function (scene) { return columns(scene, "shot__pipe"); },
    kiosk: kiosk,
    chat: chat,
    doc: doc,
    endpoints: endpoints
  };

  window.renderProjectMock = function (project, large) {
    var scene = SHOTS[project.id] || {};
    var layout = project.layout || "dashboard";
    var draw = layouts[layout] || dashboard;
    return '<div class="shot shot--' + layout + (large ? " shot--lg" : "") + '" data-accent="' + (project.accent || "cyan") + '">' + chrome(scene.title || project.mockTitle || "Sample") + draw(scene) + "</div>";
  };

    window.PORTFOLIO = [
    {
      id: "empowerid",
      title: "EmpowerID",
      type: "Identity and Access Management",
      summary: "Enterprise identity administration for deciding who can reach systems, roles, and sensitive operations.",
      status: "professional",
      statusLabel: "Professional Project",
      categories: ["enterprise", "apis"],
      stack: ["C#", ".NET", "SQL Server", "REST APIs"],
      page: "projects/empowerid.html",
      layout: "dashboard",
      mockTitle: "Access",
      accent: "cyan"
    },
    {
      id: "profile-management",
      title: "Profile Management System",
      type: "Profile and account administration",
      summary: "A single place to maintain person and account records, with permissions around who can see and change them.",
      status: "professional",
      statusLabel: "Professional Project",
      categories: ["enterprise", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/profile-management.html",
      layout: "dashboard",
      mockTitle: "Profiles",
      accent: "blue"
    },
    {
      id: "solidarity",
      title: "Solidarity",
      type: "Insurance management",
      summary: "Insurance administration software for policy records, people, and the operational steps staff move through each day.",
      status: "professional",
      statusLabel: "Professional Project",
      categories: ["enterprise", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/solidarity.html",
      layout: "board",
      mockTitle: "Policies",
      accent: "teal"
    },
    {
      id: "metro-kiosk",
      title: "Metro Kiosk Platform",
      type: "Public kiosk software",
      summary: "A fixed-screen kiosk experience for short, guided tasks, backed by services that talk to the operational systems behind it.",
      status: "professional",
      statusLabel: "Professional Project",
      categories: ["enterprise", "automation"],
      stack: ["ASP.NET Core", "Web UI", "SQL Server"],
      page: "projects/metro-kiosk.html",
      layout: "kiosk",
      mockTitle: "Kiosk",
      accent: "amber"
    },
    {
      id: "integrityweb",
      title: "IntegrityWeb",
      type: "Case management",
      summary: "A shared case record for intake, ownership, status, and notes, so operational work is not trapped in private inboxes.",
      status: "professional",
      statusLabel: "Professional Project",
      categories: ["enterprise", "analytics"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/integrityweb.html",
      layout: "board",
      mockTitle: "Cases",
      accent: "violet"
    },
    {
      id: "ai-knowledge-assistant",
      title: "AI-Powered Business Knowledge Assistant",
      type: "Internal knowledge assistant",
      summary: "A private assistant over a company's approved documents, so staff can ask questions and see the source behind an answer.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["ai", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/ai-knowledge-assistant.html",
      layout: "chat",
      mockTitle: "Knowledge",
      accent: "cyan"
    },
    {
      id: "ai-document-processing",
      title: "AI Document Processing and Data Extraction",
      type: "Document intake",
      summary: "Turns incoming files into structured fields a business system can store, with a person confirming the result before it is final.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["ai", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/ai-document-processing.html",
      layout: "doc",
      mockTitle: "Extract",
      accent: "blue"
    },
    {
      id: "saas-billing",
      title: "SaaS Subscription and Billing Dashboard",
      type: "Subscription operations",
      summary: "Plans, subscriptions, invoices, and account status for a software product that charges on a recurring basis.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["saas", "analytics"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/saas-billing.html",
      layout: "dashboard",
      mockTitle: "Billing",
      accent: "teal"
    },
    {
      id: "crm-pipeline",
      title: "CRM and Sales Pipeline",
      type: "Sales operations",
      summary: "Leads moving through defined stages, with an owner and a next action, instead of a spreadsheet that drifts out of date.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["saas", "automation", "analytics"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/crm-pipeline.html",
      layout: "pipeline",
      mockTitle: "Pipeline",
      accent: "violet"
    },
    {
      id: "inventory-warehouse",
      title: "Inventory and Warehouse Management",
      type: "Stock operations",
      summary: "SKU records, locations, and stock movements so a warehouse can see what arrived, what left, and what is running low.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["enterprise", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/inventory-warehouse.html",
      layout: "dashboard",
      mockTitle: "Stock",
      accent: "amber"
    },
    {
      id: "hr-leave",
      title: "HR and Leave Management",
      type: "People operations",
      summary: "Leave requests, balances, and approvals in one flow, so managers are not reconstructing time off from chat messages.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["enterprise", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/hr-leave.html",
      layout: "board",
      mockTitle: "Leave",
      accent: "rose"
    },
    {
      id: "school-management",
      title: "School Management System",
      type: "Education administration",
      summary: "Student records, classes, attendance, and basic academic information for a school office that has outgrown paper and scattered files.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["enterprise"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/school-management.html",
      layout: "dashboard",
      mockTitle: "School",
      accent: "blue"
    },
    {
      id: "appointment-booking",
      title: "Appointment Booking Platform",
      type: "Scheduling",
      summary: "Services, availability, and bookings for clinics, consultancies, and other businesses that live by the calendar.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["saas", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/appointment-booking.html",
      layout: "kiosk",
      mockTitle: "Bookings",
      accent: "teal"
    },
    {
      id: "ecommerce-catalog",
      title: "E-Commerce Product Catalog",
      type: "Commerce catalog",
      summary: "A maintainable product catalog with categories, search, and an admin path for merchandising, ready to connect to checkout when needed.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["saas"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/ecommerce-catalog.html",
      layout: "board",
      mockTitle: "Catalog",
      accent: "amber"
    },
    {
      id: "referral-affiliate",
      title: "Referral and Affiliate Tracking",
      type: "Partner growth",
      summary: "Tracks who referred a customer and which reward is due, with a clear status from click to qualified conversion.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["saas", "analytics"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/referral-affiliate.html",
      layout: "dashboard",
      mockTitle: "Referrals",
      accent: "violet"
    },
    {
      id: "notifications-dashboard",
      title: "Real-Time Notifications Dashboard",
      type: "Operations alerts",
      summary: "A live view of business and system events, with filters and read state, so the right people see what changed.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["analytics", "apis"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/notifications-dashboard.html",
      layout: "endpoints",
      mockTitle: "Signals",
      accent: "cyan"
    },
    {
      id: "analytics-dashboard",
      title: "Business Analytics Dashboard",
      type: "Management reporting",
      summary: "Operational numbers the business already stores, presented with filters and trends a manager can read without exporting five spreadsheets.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["analytics"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/analytics-dashboard.html",
      layout: "dashboard",
      mockTitle: "Insights",
      accent: "blue"
    },
    {
      id: "legacy-modernization",
      title: "Legacy .NET Application Modernization",
      type: "Platform modernization",
      summary: "A staged path from an older .NET application to ASP.NET Core, extracting APIs and replacing the interface without a reckless rewrite.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["apis", "enterprise"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/legacy-modernization.html",
      layout: "endpoints",
      mockTitle: "Modernize",
      accent: "rose"
    },
    {
      id: "document-portal",
      title: "Secure Document Management Portal",
      type: "Controlled document sharing",
      summary: "Folders, permissions, and an audit trail for sharing business documents with staff or external parties.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["enterprise", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/document-portal.html",
      layout: "doc",
      mockTitle: "Documents",
      accent: "teal"
    },
    {
      id: "api-integration-hub",
      title: "REST API Integration and Automation Hub",
      type: "Integration operations",
      summary: "A place to see, run, and review integrations between business systems, including failures that need a person.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["apis", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/api-integration-hub.html",
      layout: "endpoints",
      mockTitle: "Integrations",
      accent: "cyan"
    },
    {
      id: "multitenant-admin",
      title: "Multi-tenant SaaS Admin Console",
      type: "SaaS administration",
      summary: "An operator console for a product that serves many customer organizations, with tenant settings and isolated data access.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["saas", "apis"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/multitenant-admin.html",
      layout: "dashboard",
      mockTitle: "Tenants",
      accent: "violet"
    },
    {
      id: "payment-reconciliation",
      title: "Payment Reconciliation Workspace",
      type: "Finance operations",
      summary: "Matches provider payouts and statement lines to invoices, and leaves a clear queue for the exceptions finance still has to judge.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["analytics", "apis"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/payment-reconciliation.html",
      layout: "doc",
      mockTitle: "Reconcile",
      accent: "amber"
    },
    {
      id: "remote-sprint-workspace",
      title: "Remote Sprint Workspace",
      type: "Remote team delivery",
      summary: "A sprint board for a distributed team: stories, owners, and a daily status that does not depend on everyone sitting in the same office.",
      status: "demo",
      statusLabel: "Demo Project",
      categories: ["remote", "saas", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server", "Azure"],
      page: "projects/remote-sprint-workspace.html",
      layout: "board",
      mockTitle: "Sprint",
      accent: "cyan"
    },
    {
      id: "client-delivery-portal",
      title: "Client Delivery Portal",
      type: "Remote client delivery",
      summary: "A client portal for milestone reviews, file handoff, and written decisions when the team and the client are not in the same city.",
      status: "demo",
      statusLabel: "Demo Project",
      categories: ["remote", "saas"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/client-delivery-portal.html",
      layout: "dashboard",
      mockTitle: "Delivery",
      accent: "blue"
    },
    {
      id: "enterprise-procurement",
      title: "Enterprise Procurement",
      type: "Enterprise purchasing",
      summary: "Purchase requests, vendor records, and approval steps for an organization that needs a trail from request to order.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["enterprise", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/enterprise-procurement.html",
      layout: "board",
      mockTitle: "Procurement",
      accent: "amber"
    },
    {
      id: "multisite-operations",
      title: "Multi-site Operations Console",
      type: "Enterprise operations",
      summary: "One console for several branches, with open work, staffing notes, and the exceptions a regional lead needs to see.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["enterprise", "analytics"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/multisite-operations.html",
      layout: "dashboard",
      mockTitle: "Sites",
      accent: "teal"
    },
    {
      id: "saas-onboarding",
      title: "SaaS Tenant Onboarding",
      type: "SaaS onboarding",
      summary: "Guided setup for a new tenant: company profile, users, and the first integration, without a support call for every account.",
      status: "demo",
      statusLabel: "Demo Project",
      categories: ["saas", "apis"],
      stack: ["ASP.NET Core", "Angular", "SQL Server", "REST"],
      page: "projects/saas-onboarding.html",
      layout: "dashboard",
      mockTitle: "Onboarding",
      accent: "violet"
    },
    {
      id: "ai-support-triage",
      title: "AI Support Triage",
      type: "AI-assisted support",
      summary: "Incoming support messages get a suggested category and a draft reply. A person approves the reply before it is sent.",
      status: "demo",
      statusLabel: "Demo Project",
      categories: ["ai", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server", "Language-model API"],
      page: "projects/ai-support-triage.html",
      layout: "chat",
      mockTitle: "Support",
      accent: "cyan"
    },
    {
      id: "ai-requirements-assistant",
      title: "AI Requirements Assistant",
      type: "AI product discovery",
      summary: "Turns a rough brief into a structured backlog draft: goals, open questions, and suggested stories a product owner can edit.",
      status: "concept",
      statusLabel: "Concept Project",
      categories: ["ai", "apis"],
      stack: ["ASP.NET Core", "Angular", "SQL Server", "Language-model API"],
      page: "projects/ai-requirements-assistant.html",
      layout: "doc",
      mockTitle: "Brief",
      accent: "violet"
    },
    {
      id: "service-business-suite",
      title: "Service Business Suite",
      type: "Full-stack service application",
      summary: "Booking, a staff calendar, and invoices in one application for a service business that currently runs on chat and spreadsheets.",
      status: "demo",
      statusLabel: "Demo Project",
      categories: ["saas", "automation"],
      stack: ["ASP.NET Core", "Angular", "SQL Server"],
      page: "projects/service-business-suite.html",
      layout: "dashboard",
      mockTitle: "Services",
      accent: "teal"
    }
  ];

  window.PORTFOLIO.forEach(function (project) {
    project.pageFromRoot = project.page;
  });

  var grid = document.getElementById("project-grid");
  if (!grid) return;

  var prefix = grid.getAttribute("data-prefix") || "";
  grid.innerHTML = window.PORTFOLIO.map(function (project) {
    var href = prefix + project.page;
    var scene = SHOTS[project.id] || {};
    var features = scene.features || [];
    var featureHtml = features.length
      ? '<ul class="feature-list">' + features.slice(0, 3).map(function (item) {
          return "<li>" + escapeHtml(item) + "</li>";
        }).join("") + "</ul>"
      : "";
    return (
      '<article class="project-card" data-status="' + project.status + '" data-accent="' + (project.accent || "cyan") + '" data-categories="' + project.categories.join(" ") + '">' +
      '<figure class="project-card__media">' +
      window.renderProjectMock(project, false) +
      "<figcaption>Sample interface</figcaption></figure>" +
      '<div class="project-card__body">' +
      '<div class="project-card__meta">' +
      '<p class="badge badge--' + project.status + '">' + escapeHtml(project.statusLabel) + "</p>" +
      '<p class="project-card__type">' + escapeHtml(project.type) + "</p></div>" +
      '<h3><a href="' + href + '">' + escapeHtml(project.title) + "</a></h3>" +
      '<p class="project-card__summary">' + escapeHtml(project.summary) + "</p>" +
      featureHtml +
      '<ul class="pills">' + project.stack.map(function (item) { return "<li>" + escapeHtml(item) + "</li>"; }).join("") + "</ul>" +
      '<a class="text-link" href="' + href + '">View case study</a>' +
      "</div></article>"
    );
  }).join("");
})();
