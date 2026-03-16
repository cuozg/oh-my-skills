# Feature X

## Technical Architecture Design

## Review Status

| Reviewer | Approved | Last Reviewed | Re-review Ready |
| :---: | :---- | :---: | ----- |
|  |  | Date |  |
|  |  | Date |  |
|  |  | Date |  |
|  |  | Date |  |
|  |  | Date |  |
|  |  | Date |  |
|  |  | Date |  |
|  |  | Date |  |

## Important Links

| Design 1-pager: |  |
| :---- | :---- |
| Design brief: |  |
| Design spec: |  |
| Miro: |  |
| Task Breakdown: |  |
| Other: |  |

## Feature Summary and High level details

Brief summary of the feature to help build context and lay the foundation for what we are going to discuss in this doc.

### Existing Tech Being Used Largely As-is

Describe existing tech you are planning on integrating with as-is (e.g. it will use existing battle logic) or using only a previous game mode as basis.

Describe existing tech you are planning to copy and use as a starting point, if any. Include some description of pros/cons of using this existing system.  
Full details to be added in feature component section

### Existing Tech Being Changed

Describe existing tech you will be revamping or removing. (e.g. existing shop functionality will be upgraded to support event currency tabs.)  
Full details to be added in feature component section

### New Tech 

Briefly outline the new tech to be built for the feature   
Full details to be added in feature component section

### Playgami/Central/External Integrations

List all Playgami or Central or external tech we integrate for this feature.  
Briefly outline the need and benefits of the integrations. Add relevant documentation and guides

### Feature Compatibility with Time-Offset feature

Features with a schedule to be run by Live-ops should work with a time-offset feature.   
Highlight any compatibility risks/concerns if any Or Just mark this as Compatible  
NOTE: Time-offset is a debug option only available in non-prod environments.

## Key Architectural Decisions

### Foundational Assumptions

Describe each assumption if any you are relying on in this TDD document. It serves as a design and tech constraint/guideline going forward. Example: building this tech can only allow us to one 1 single event and wouldn’t scale Or handle only specific type of rewards

This list is meant to highlight assumptions that go beyond spec and can affect feature development in future both from design and tech perspective

You can provide more details about the architectural complexity you are avoiding by making this limitation.   
Example: We are storing data on the client and therefore can’t guarantee its security but it enables us to reduce costs. While code is never set in stone, adapting it to move this data to the server would essentially amount to rewriting the feature from scratch.

### 

### Performance Constraints/Risks

Applies to both Client and Server. List all client and server risks as applicable.  
Call out any constraints and risks from a performance perspective. Think about   
\- Data storage considerations  
\- Stress testing  
\- Backward Compatibility  
\- Force or No force update considerations  
\- API overload concerns  
\- Data corruption  
\- Out of syncs issues  
\- Scalability concerns  
\- Security concerns  
\- Memory usage   
\- FPS  
\- CPU Usage  
\- Behaviour and tech challenges on low, mid end devices

# Feature Components

Divide features into components, and highlight details of all components in this section. A component is a portion of a spec which can be used as an umbrella under which feature functionality can be defined. Show UI wireframes for better understanding of these components.  
Every component the below details as when applicable:  
Client

\-  How is data populated for UI models  
\-  How and when is screen UI and data models refreshed?  
\-  What components of the screen are static vs dynamic. Is Prefab setup in a way so the static UI is unaffected by any transition changes when the UI is refreshed?  
\-  How are UI assets loaded/unloaded and when?  
\- Notable prefab setup details  
\-  Client-server interactions  
\- Add flow/sequence diagram/s   
\- What new API/s are added to interact with the server?  
\- How often are they called?  
\- Can all clients request the same data at the same time?  
\-  How are we handling/limiting players' interaction with screens to prevent API trigger overload. Example spam tapping.  
\-  How are we treating error handling eg Asset not loaded, UI data not available, API request failure, CTA failures?   
\-  Offline handling?  
\-  Feature kill-switch handling?  
	\- How does client UI behave?  
	\- Will it kill all server API requests for the feature?  
\-  Local client cache clear handling?  
\-  Local Clock time change handling?  
\-  Debug functionality created for dev and QA testing?  
\-  Do we have data available for all telemetry needs?  
\-  Out of sync considerations?

Server

\-  What is our feature configuration data?  
\-  Where is feature configuration data stored?  
	\- Is data compressed?  
	\- Are we sending all the data OR just what the client needs?  
\-  What is our player/feature progress specific data?  
	\- List all fields Or JSON schema   
\-  Where is all player/feature specific data stored?  
	\- Are we sending all the data OR just what the client needs?  
	\- List all data stores(databases, caches) and reasons for choosing those.  
\-  How can player data be edited or cleaned up?   
	\- Can CS edit this in production env through a tool? Any limitations?  
	\- Can QA edit this in dev/QA env?  
	\- TTL for all data fields?   
\-  Any cron jobs created for data aggregation/cleanup?  
\-  Define client-server interaction  
\- Add flow/sequence diagram/s   
\- What new API are created and it’s use-cases  
	\- Request and Response payload?  
\-  Detail external web-hooks or services integration needed?  
	\- Playgami, central OR external 3rd party  
\-  Any debug functionality added?  
\- Do we have data available for all telemetry needs?  
\- Feature kill-switch handling?  
	\- Will we stop sending any blueprint or player progress data to the client?  
\- Out of sync considerations?

### WebGL Considerations

Potential Web Client considerations and any risks to WebGL performance and deployment

### Tech Launch and Monitoring Plans

\- Any special launch readiness plan needed?  
\- How are we going to monitor feature stability?  
\- What dashboards are created or used for client and server  
\- How do we plan to use those?  
  

### Analytics Implementation

\- Any new data hooks we need to create for analytics events?  
\- How are we verifying that analytics events are getting logged?  
\- Any new tech/system we are creating to meet analytic requirements?

### Additional Technical Specification

### API Reference

Consolidated list of all new and modified APIs across all components:

**New APIs:**

- API endpoint 1: \[endpoint description\]  
- API endpoint 2: \[endpoint description\]

**Modified APIs:**

- API endpoint 3: \[modification description\]

**Request/Response Examples:**

```json
// Example API payload
```

**Error Handling Patterns:**

- Standard error codes and responses

Data Architecture  
Consolidated list of all new and modified blueprint data across all components:

- \[Update\] blueprint\_name.json: \[description of changes\]  
- \[New\] new\_blueprint.json: \[description of new blueprint\]

